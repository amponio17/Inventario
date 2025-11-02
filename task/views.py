import csv
import logging
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from .models import *
from .forms import ItemForm, StockForm
from datetime import datetime, timedelta
from django.utils import timezone
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Create your views here.

logger = logging.getLogger(__name__)

@login_required
def inicio(request):
   
    grafico_html = histograma_movimientos()
    return render(request, "paginas/PagP.html", {"grafico": grafico_html})

# @login_required
# def login(request):
   
#     return render(request, 'paginas/log.html',
        
#     )

# @login_required
def productos(request):
   
    query = request.GET.get('q', '')
    stock_list = stock.objects.select_related('stock_item_id', 'stock_position_id')

    if query:
        stock_list = stock_list.filter(
            Q(stock_item_id__item_name__icontains=query)
        )

    paginator = Paginator(stock_list, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'productos/vistaP.html', {
        'page_obj': page_obj,
        'query': query,
    })

@login_required
def historial(request):
    
    qs = stock_tracking.objects.select_related(
        "st_id_stock__stock_item_id",
        "st_id_user"
    ).order_by("-created_at")

    # Filtrado por producto (pk o parte de nombre) - usar product_id si pasas id exacto
    product = request.GET.get("product", "").strip()
    if product:
        # Si envías id numérico:
        if product.isdigit():
            qs = qs.filter(st_id_stock__stock_item_id__pk=int(product))
        else:
            # filtro por nombre parcial (case-insensitive)
            qs = qs.filter(st_id_stock__stock_item_id__item_name__icontains=product)

    # Filtrado por usuario (username o id)
    user = request.GET.get("user", "").strip()
    if user:
        if user.isdigit():
            qs = qs.filter(st_id_user__pk=int(user))
        else:
            qs = qs.filter(st_id_user__username__icontains=user)

    # Rango de fechas (espera formato YYYY-MM-DD)
    start = request.GET.get("start_date", "").strip()
    end = request.GET.get("end_date", "").strip()
    try:
        if start:
            dt_start = timezone.make_aware(datetime.strptime(start, "%Y-%m-%d"))
            qs = qs.filter(created_at__gte=dt_start)
        if end:
            # incluir el día completo: hasta 23:59:59
            dt_end = timezone.make_aware(datetime.strptime(end, "%Y-%m-%d"))
            dt_end = dt_end.replace(hour=23, minute=59, second=59)
            qs = qs.filter(created_at__lte=dt_end)
    except ValueError:
        # Si el formato es incorrecto, ignorar el filtro; podrías mostrar un mensaje
        pass

    # Export CSV si se solicita
    if request.GET.get("export", "").lower() == "csv":
        return _export_movimientos_csv(qs)

    # Paginación
    paginator = Paginator(qs, 10)
    page_number = int(request.GET.get("page", 1))
    page_obj = paginator.get_page(page_number)

    # Calcular rango de páginas centrado en la página actual (ventana de 5 páginas)
    total = paginator.num_pages
    start = max(1, page_obj.number - 2)
    end = min(total, page_obj.number + 2)
    page_range = range(start, end + 1)

    productos = stock.objects.select_related("stock_item_id").values_list(
        "stock_item_id__pk", "stock_item_id__item_name"
    ).distinct()
    usuarios = User.objects.values_list("pk", "username").order_by("username")[:200]

    context = {
        "page_obj": page_obj,
        "productos": productos,
        "usuarios": usuarios,
        "filters": {"product": request.GET.get("product", ""), "user": request.GET.get("user", ""),
                    "start_date": request.GET.get("start_date", ""), "end_date": request.GET.get("end_date", "")},
        "page_range": page_range,
    }
    return render(request, "paginas/historial.html", context)



def _export_movimientos_csv(queryset):
    """
    Exporta el queryset (ya filtrado) a CSV y devuelve HttpResponse.
    Columnas: ID, Producto, Usuario, Cantidad antes, Cantidad después, Fecha
    """
    # Crear response CSV
    filename = f"movimientos_stock_{timezone.now().strftime('%d-%m-%Y_%H%M%S')}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(["ID", "Producto", "Usuario", "Cantidad antes", "Cantidad después", "Fecha"])

    for mov in queryset.iterator():
        producto = "-"
        try:
            producto = mov.st_id_stock.stock_item_id.item_name
        except Exception:
            producto = "-"
        usuario = getattr(mov.st_id_user, "username", "-")
        writer.writerow([
            mov.st_id,
            producto,
            usuario,
            mov.st_prev,
            mov.st_act,
            mov.created_at.isoformat()
        ])

    return response

    
def histograma_movimientos():
    # Fecha límite (últimos 30 días)
    fecha_limite = timezone.now() - timedelta(days=30)

    # Queryset de movimientos recientes
    movimientos = stock_tracking.objects.filter(created_at__gte=fecha_limite).select_related("st_id_stock__stock_item_id")

    # Calcular la diferencia de stock en cada movimiento
    data = [
        {
            "producto": m.st_id_stock.stock_item_id.item_name,
            "cambio": m.st_act - m.st_prev,
            "fecha": m.created_at
        }
        for m in movimientos
    ]
    df = pd.DataFrame(data)
    
    df = df[df["cambio"] != 0]

    if df.empty:
        # Gráfico vacío con texto aclaratorio si no hay movimientos con cambio
        fig = px.bar(x=[0], y=[0])
        fig.update_layout(
            title="No hay movimientos con cambio en los últimos 30 días",
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[{
                "text": "No se encontraron cambios distintos de 0",
                "xref": "paper", "yref": "paper", "showarrow": False, "x": 0.5, "y": 0.5
            }]
        )
    else:
        nbins = 100
        bin_edges = np.histogram_bin_edges(df["cambio"], bins=nbins)
        # Calcular bin center para etiquetar eje x
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        # Añadir columna con el índice del bin
        df["bin"] = pd.cut(df["cambio"], bins=bin_edges, include_lowest=True, labels=False)

        # Agregar por producto y bin: count y última fecha
        agg = df.groupby(["producto", "bin"], as_index=False).agg(
            count=("cambio", "size"),
            last_date=("fecha", "max")
        )
        # Para trazar, creamos una traza por producto con x = bin_centers[bin]
        fig = go.Figure()
        productos = agg["producto"].unique()
        for prod in productos:
            sub = agg[agg["producto"] == prod]
            if sub.empty:
                continue
            x = [bin_centers[int(b)] for b in sub["bin"]]
            y = sub["count"].tolist()
            last_dates = sub["last_date"].dt.strftime("%Y-%m-%d %H:%M:%S").tolist()

            # Hover personalizado: muestra producto, rango de bin (approx), count y última fecha
            hover_text = []
            for b_idx, cnt, ld in zip(sub["bin"], y, last_dates):
                left = bin_edges[int(b_idx)]
                right = bin_edges[int(b_idx) + 1]
                hover_text.append(
                    f"Producto: {prod}<br>Cambio en stock ∈ [{left:.1f}, {right:.1f})<br>Count: {cnt}<br>Último movimiento: {ld}"
                )

            fig.add_trace(go.Bar(
                x=x,
                y=y,
                name=prod,
                text=y,
                hovertext=hover_text,
                hoverinfo="text",
                marker_line_width=0.5,
                opacity=0.85
            ))
        
        fig.update_layout(
            barmode="overlay",
            title="Histograma de cambios en stock por producto (últimos 30 días)",
            xaxis_title="Cambio en stock (bin center)",
            yaxis_title="Frecuencia",
            legend_title_text="Producto"
        )





    return fig.to_html(full_html=False)


@login_required
def agregar(request):
        if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Producto agregado exitosamente.")
                return redirect('agregar')  # Redirige a la vista de productos después de guardar
            else:
                messages.error(request, "Error al agregar el producto. Por favor, verifica los datos ingresados.")
        else:
            form = ItemForm()  # Vuelve a mostrar el formulario vacío si no es válido
        return render(request, 'productos/agregar.html', {'form': form})

User = get_user_model()

@login_required
def editar_stock(request, pk):
    item = get_object_or_404(stock, pk=pk)

    if request.method == 'POST':
        form = StockForm(request.POST, instance=item)
        if form.is_valid():
            # Leer valor anterior desde BD para evitar inconsistencias
            item.refresh_from_db(fields=['stock_item_amount'])
            stock_anterior = item.stock_item_amount

            with transaction.atomic():
                # Guardar y asegurarse de que la instancia se actualice en BD
                saved_item = form.save()           # guarda y devuelve la instancia
                saved_item.refresh_from_db(fields=['stock_item_amount'])

                # Obtener el nuevo valor preferentemente desde cleaned_data
                stock_nuevo = form.cleaned_data.get('stock_item_amount', saved_item.stock_item_amount)

                # Si por alguna razón cleaned_data no existe, intentar parsear request.POST
                if stock_nuevo is None and 'stock_item_amount' in request.POST:
                    try:
                        stock_nuevo = int(request.POST.get('stock_item_amount'))
                    except (ValueError, TypeError):
                        stock_nuevo = saved_item.stock_item_amount
                
                # Confirmar que la instancia en BD tiene el nuevo valor
                if saved_item.stock_item_amount != stock_nuevo:
                    # Si no coincide, forzar asignación y salvar
                    saved_item.stock_item_amount = stock_nuevo
                    saved_item.save()
                    saved_item.refresh_from_db()

                # Crear tracking sólo si hay cambio real
                if stock_anterior != stock_nuevo:
                    # Evitar duplicados inmediatos
                    ultimo = stock_tracking.objects.filter(
                        st_id_stock=saved_item,
                        st_prev=stock_anterior,
                        st_act=stock_nuevo
                    ).order_by('-created_at').first()
                    if not ultimo:
                        stock_tracking.objects.create(
                            st_id_stock=saved_item,
                            st_id_user=request.user,
                            st_prev=stock_anterior,
                            st_act=stock_nuevo
                        )

            return redirect('productos')
    else:
        form = StockForm(instance=item)

    return render(request, 'productos/editar.html', {'form': form})




    
@login_required
def eliminar_stock(request, pk):
    item = get_object_or_404(stock, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('productos')
    return render(request, 'productos/eliminar.html', {'item': item})


def logout_request(request):
     logout(request)
     return render(request,'paginas/saliste.html')