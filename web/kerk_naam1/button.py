def html(button_class, value, label):
    return f"""
    <button class="{button_class}" type="submit" name="action" value={value}>{label}</button>
    """