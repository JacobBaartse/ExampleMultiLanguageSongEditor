def html(name, checked, label):
    return f"""
    <label class="cr-wrapper">
  <input type="checkbox" name="{name}" value="{name}" {checked}/>
  <div class="cr-input"></div>
  <span>{label}</span>
</label>
"""
