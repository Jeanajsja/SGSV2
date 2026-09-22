def validar_dominio_email(email):
    email = (email or "").lower()
    if "@" not in email:
        return None

    dominio_completo = email.split("@")[-1]
    dominio_base = dominio_completo.split(".")[0]

    typos_base = {
        "gmal": "gmail",
        "gmai": "gmail",
        "gamil": "gmail",
        "gmaill": "gmail",
        "hotml": "hotmail",
        "hotmal": "hotmail",
        "hormail": "hotmail",
        "homail": "hotmail",
        "outlok": "outlook",
        "outloo": "outlook",
        "oulook": "outlook",
        "yaho": "yahoo",
        "yahhoo": "yahoo",
    }

    if dominio_base in typos_base:
        correccion = dominio_completo.replace(dominio_base, typos_base[dominio_base], 1)
        return {"status": "error", "message": f"Dominio de correo inválido. ¿Quisiste escribir @{correccion}?"}

    if dominio_completo.endswith((".con", ".c", ".om", ".o")):
        correccion = dominio_completo.rsplit(".", 1)[0] + ".com"
        return {"status": "error", "message": f"Dominio de correo inválido. ¿Quisiste escribir @{correccion}?"}

    return None
