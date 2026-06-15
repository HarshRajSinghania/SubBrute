from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import os
import tempfile
from subbrute import run_subbrute

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # In production, use a proper secret key

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form.get('domain', '').strip()
        threads = request.form.get('threads', '50')
        timeout = request.form.get('timeout', '5')
        wordlist_file = request.files.get('wordlist')

        # Validate inputs
        if not domain:
            flash('Domain is required', 'danger')
            return redirect(url_for('index'))

        try:
            threads = int(threads)
            if threads < 1:
                raise ValueError
        except ValueError:
            flash('Threads must be a positive integer', 'danger')
            return redirect(url_for('index'))

        try:
            timeout = int(timeout)
            if timeout < 1:
                raise ValueError
        except ValueError:
            flash('Timeout must be a positive integer', 'danger')
            return redirect(url_for('index'))

        # Determine wordlist path
        if wordlist_file and wordlist_file.filename != '':
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp:
                wordlist_file.save(tmp.name)
                wordlist_path = tmp.name
                wordlist_name = wordlist_file.filename
                # We'll need to delete this file after use
                cleanup_tmp = True
        else:
            # Use default wordlist
            wordlist_path = 'wordlist.txt'
            wordlist_name = 'wordlist.txt (default)'
            cleanup_tmp = False

        # Check if wordlist exists
        if not os.path.exists(wordlist_path):
            flash(f'Wordlist file not found: {wordlist_path}', 'danger')
            if cleanup_tmp:
                os.unlink(wordlist_path)
            return redirect(url_for('index'))

        # Run subbrute
        try:
            results = run_subbrute(domain, wordlist_path, threads, timeout)
        except Exception as e:
            flash(f'Error during enumeration: {str(e)}', 'danger')
            if cleanup_tmp:
                os.unlink(wordlist_path)
            return redirect(url_for('index'))
        finally:
            if cleanup_tmp:
                try:
                    os.unlink(wordlist_path)
                except:
                    pass

        # Render results
        return render_template('index.html', 
                               results=results, 
                               domain=domain,
                               wordlist_name=wordlist_name,
                               threads=threads,
                               timeout=timeout)

    # GET request
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)