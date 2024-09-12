def total_carrito(request):
    total = 0
    if request.user.is_authenticated:
        if "carrito" in request.session:
            print("Carrito encontrado en la sesión:", request.session["carrito"])
            for key, value in request.session["carrito"].items():
                total += int(value["acumulado"])
    print("Total del carrito:", total)
    return {"total_carrito": total}