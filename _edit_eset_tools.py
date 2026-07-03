from pathlib import Path  
  
path = Path('modules/EsetTools.py')  
lines = path.read_text(encoding='utf-8').splitlines(True)  
  
for i, line in enumerate(lines):  
    if line == \"import sys\n\":  
        import_index = i + 1  
        break  
else:  
    import_index = None  
if import_index is not None and \"from datetime import datetime\n\" not in lines:  
    lines.insert(import_index, \"from datetime import datetime\n\")  
  
for i, line in enumerate(lines):  
    if line == \"class EsetRegister(object):\n\":  
        register_index = i  
        break  
else:  
    register_index = None  
helper_lines = [  
    \"\",  
    \"def dump_current_html(driver_obj, reason: str):\",  
    \"    debug_dir = Path('debug_html')\",  
    \"    debug_dir.mkdir(exist_ok=True)\",  
    \"    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')\",  
    \"    safe_reason = reason.replace('/', '_').replace(' ', '-')\",  
    \"    file_path = debug_dir / f'{safe_reason}_{timestamp}.html'\",  
    \"    try:\",  
    \"        url = ''\",  
    \"        try:\",  
    \"            url = driver_obj.current_url\",  
    \"        except:\",  
    \"            pass\",  
    \"        html = ''\",  
    \"        try:\",  
    \"            html = driver_obj.page_source\",  
    \"        except:\",  
    \"            html = f'Failed to read page source on {timestamp}'\",  
    \"        file_path.write_text(\",  
    \"            f'Snapshot: {timestamp}' + chr(10) +\",  
    \"            f'Reason: {reason}' + chr(10) +\",  
    \"            f'URL: {url}' + chr(10) + chr(10) +\",  
    \"            f'{html}',\",  
    \"            encoding='utf-8',\",  
    \"            errors='ignore'\",  
    \"        )\",  
    \"        logging.warning(f'[DEBUG_HTML] Saved page source at {file_path}')\",  
    \"        return str(file_path)\",  
    \"    except Exception as error:\",  
    \"        logging.error(f'[DEBUG_HTML] Cannot save html: {error}')\",  
    \"        return None\",  
]  
if register_index is not None and \"def dump_current_html\" not in ''.join(lines[:register_index]):  
    lines[register_index:register_index] = [line + '\n' for line in helper_lines]  
  
target_click = \"        uCE(self.driver, f\\\"return {CLICK_WITH_BOOL}({DEFINE_GET_EBAV_FUNCTION}('button', 'data-label', 'register-continue-button'))\\\")\"  
new_click_lines = [  
    \"        try:\",  
    \"            uCE(self.driver, f\\\"return {CLICK_WITH_BOOL}({DEFINE_GET_EBAV_FUNCTION}('button', 'data-label', 'register-continue-button'))\\\")\",  
    \"        except:\",  
    \"            debug_file = dump_current_html(self.driver, 'register-continue-button-missing')\",  
    \"            if debug_file:\",  
    \"                console_log(f'DEBUG_HTML saved: {debug_file}', ERROR, silent_mode=SILENT_MODE)\",  
    \"            clicked = False\",  
    \"            for _ in range(12):\",  
    \"                for button in self.driver.find_elements('tag name', 'button'):\",  
    \"                    try:\",  
    \"                        if not button.is_displayed() or not button.is_enabled():\",  
    \"                            continue\",  
    \"                        label = (button.get_attribute('data-label') or '').lower()\",  
    \"                        text = (button.get_attribute('innerText') or button.text or '').strip().lower()\",  
    \"                        if 'register-continue-button' in label or text == 'continue' or 'continue' in label:\",  
    \"                            button.click()\",  
    \"                            clicked = True\",  
    \"                            break\",  
    \"                    except:\",  
    \"                        continue\",  
    \"                if clicked:\",  
    \"                    break\",  
    \"                time.sleep(DEFAULT_DELAY)\",  
    \"            if not clicked:\",  
    \"                raise RuntimeError('Unable to find/click register continue button. Snapshot for debug has been saved.')\",  
]  
for i, line in enumerate(lines):  
    if target_click in line:  
        lines[i:i+1] = [line + '\n' for line in new_click_lines]  
        break  
else:  
    print('target click line not found')  
  
path.write_text(''.join(lines), encoding='utf-8') 
