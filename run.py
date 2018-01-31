from flask import Flask
from flask import render_template
from flask import url_for
import os
import glob

app = Flask(__name__)
STATIC = 'static/'

@app.route('/')
def glue_page():
    notebooks = get_all_notebooks()
    return render_template('everything.html', notebooks=notebooks)

def get_all_notebooks():
    relative_paths = glob.glob('%snotebooks/*' % STATIC)
    book_names = [''.join(rp.split('/')[-1]) for rp in relative_paths]
    book_urls = [url_for('.get_notebook', book=book) for book in book_names]
    date_paths = [os.path.join(rp, 'date') for rp in relative_paths]
    dates = []
    for date_path in date_paths:
        with open(date_path, 'rb') as datefile:
            dates.append(datefile.read().strip())
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
