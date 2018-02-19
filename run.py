from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
import os
import glob

STATIC = 'static/'
app = Flask(__name__)

@app.route('/')
def glue_page():
    notebooks = get_all_notebooks()
    webpages = get_all_webpages()
    return render_template('everything.html', notebooks=notebooks, webpages=webpages)

def get_dates(relative_paths):
    date_paths = [os.path.join(rp, 'date') for rp in relative_paths]
    dates = []
    for date_path in date_paths:
        try:
            with open(date_path, 'rb') as datefile:
                dates.append(datefile.read().strip())
        except Exception as e:
            dates.append('')
    return dates


def get_all_notebooks():
    relative_paths = glob.glob('%snotebooks/*' % STATIC)
    book_names = [''.join(rp.split('/')[-1]) for rp in relative_paths]
    book_urls = [url_for('.get_notebook', book=book) for book in book_names]
    dates = get_dates(relative_paths)
    zipped = sorted(zip(book_urls, book_names, dates), key=lambda x: x[2])
    return [{'book_url': z[0], 'name': z[1], 'date': z[2]} for z in zipped]

def static_url_from_relative(relative_path):
    return url_for('static', filename=relative_path.replace(STATIC, ''))

def get_urls(paths):
    # short name -> path mapping
    return dict([(os.path.basename(path).split('_')[0].split('.')[0],
                 static_url_from_relative(path))
                 for path in paths])

def get_all_image_links(notebook_name):
    """
    provides a list of dictionaries with information needed for image links
    """
    base_path = os.path.join('%snotebooks' % STATIC, notebook_name)
    thumbs = get_urls(glob.glob(os.path.join(base_path, 'thumbs/*')))
    images = get_urls(glob.glob(os.path.join(base_path, 'images/*')))
    captions = get_urls(glob.glob(os.path.join(base_path, 'captions/*')))
    merged = [{'alt': k, 'thumb': thumbs[k],
               'image': images.get(k), 'caption': captions.get(k)}
              for k in thumbs]
    return merged

# static webpages
def get_all_webpages():
    relative_paths = glob.glob('%swebpages/*' % STATIC)
    page_names = [''.join(rp.split('/')[-1]) for rp in relative_paths]
    page_urls = [url_for('.get_webpage', page=page) for page in page_names]
    dates = get_dates(relative_paths)
    zipped = sorted(zip(page_urls, page_names, dates), key=lambda x: x[2])
    return [{'page_url': z[0], 'name': z[1], 'date': z[2]} for z in zipped]

# https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
@app.route('/webpages/<page>')
def get_webpage(page):
    filename = 'webpages/%s/index.html' % (page)
    # another way to do this which doesn't require changing all the paths in the files
    # but makes the URLs longer
    #actual_url = url_for('static', filename=filename)
    #return redirect(actual_url)
    return app.send_static_file(filename)

@app.route('/notes/<book>')
def get_notebook(book):
    base_path = os.path.join('%snotebooks/%s' % (STATIC, book))
    repr_images = [static_url_from_relative(path) for path in 
                   glob.glob(os.path.join(base_path, '*.png'))]
    repr_image = repr_images[0] if repr_images and len(repr_images) else None
    image_links = get_all_image_links(book)
    return render_template('book.html', repr_image=repr_image, image_links=image_links)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = False)
