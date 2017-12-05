import json
from urllib import parse, request
from urllib.error import URLError
from urllib.request import urlopen

from datetime import datetime
from moleskin import moleskin as M
from tqdm import tqdm
from waterbear import DefaultBear

data_file = "notes.json"
host = "https://openreview.net/notes"
invitation = parse.quote_plus("ICLR.cc/2018/Conference/-/Blind_Submission")
debug_url = False


def get_json(url):
    try:
        with urlopen(request.Request(url)) as f:
            return json.loads(f.read().decode('utf-8'))
    except URLError as e:
        raise e


def dump_json(data):
    with open(data_file, 'w') as dump_file:
        json.dump(data, dump_file)


def load_json():
    with open(data_file, 'r') as f:
        return json.loads(f.read())


def list_submissions(offset=0, limit=50, use_cache=False, dump=False):
    params = f'invitation={invitation}&offset={offset}&limit={limit}'
    url = host + "?" + params
    if debug_url:
        M.green(url)

    if use_cache:
        with open(data_file, 'r') as dump_file:
            return json.load(dump_file)

    data = get_json(url)
    notes = data['notes']
    if dump:
        dump_json(data)
    return notes


def get_reviews(id, trash=True, use_cache=True, dump=False):
    url = host + "?" + f"forum={id}&trash={'true' if trash else 'false'}"
    if debug_url:
        M.green(url)
    data = get_json(url)
    return data


def get_all_submissions():
    all = []
    offset = 0
    limit = 2000
    while True:
        M.yellow('.', end='')
        notes = list_submissions(offset=offset, limit=limit)
        all.extend(notes)
        if len(notes) == 0:
            break
        offset += limit

    from termcolor import colored as c
    print(c(len(all), 'green'), "total submissions")
    dump_json({"notes": all})


def get_all_reviews():
    notes = load_json()['notes']
    reviews = {}
    for n in tqdm(notes):
        forum_id = n['forum']
        review_notes = get_reviews(forum_id)['notes']
        # note that number of notes limited to 2000. corner case could when one paper has 2000+ reviews
        reviews[forum_id] = review_notes
    dump_json({"notes": notes, "reviews": reviews})


def pluck(d, *keys):  # because python fucking sucks and javascript is way better.
    return [d[k] for k in keys]


class Review(DefaultBear):
    def __init__(self, review_json):
        content = review_json['content']
        super(Review, self).__init__(None, **content)


def map_review(fn: callable, fil: callable, review_json: dict):
    results = []
    for rs in review_json.values():
        for r in rs:
            review = Review(r)
            if fil(review):
                results.append(fn(review))
    return results


def map_submission(fn: callable, fil: callable, review_json: dict):
    results = []
    for rs in review_json.values():
        submission_results = []
        for r in rs:
            review = Review(r)
            if fil(review):
                submission_results.append(fn(review))
        results.append(submission_results)
    return results


if __name__ == "__main__":
    # get_all_submissions()
    # get_all_reviews()

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    save_prefix = "./figures/"

    notes, reviews = pluck(load_json(), 'notes', 'reviews')

    plt.title("ICLR 2018 Review Scores")
    ratings = map_submission(lambda r: float(r.rating[0]), lambda r: r.rating, reviews)
    flatten_view = np.hstack(ratings)
    plt.hist(flatten_view, bins=np.linspace(1, 10, 10) - 0.5, normed=True, alpha=1.0, histtype='step',
             color="#44b7ff", edgecolor='#44b7ff', linewidth=5, label="all scores")
    per_submission = [np.mean([r for r in submission]) for submission in ratings if len(submission) > 0]
    plt.hist(per_submission, bins=np.linspace(1, 10, 19) - 0.25, normed=True, alpha=0.8,
             color="#ff7272", edgecolor='white', linewidth=2, label="per submission")
    plt.xlabel('Score (1 to 10)')
    plt.ylabel('Probability')
    plt.legend(framealpha=1, frameon=False)
    plt.savefig(save_prefix + 'all_scores.png')
    plt.show()

    M.green('mean', end='')
    print(f" = {np.mean(per_submission):.2f}", )
    M.green('median', end='')
    print(f" = {np.median(per_submission):.2f}", )
    M.green('our rating', end='')
    print(f" = {np.mean([4, 6, 6]):.2f}", )

    fig, ax = plt.subplots(1, 1)
    plt.title("ICLR 2018 Submission Time Line")
    # dates = [r['tmdate'] / 1000 for sub in reviews.values() for r in sub if 'rating' in r['content']]
    # times = mdates.epoch2num([d for d in dates])
    # plt.hist(times, normed=False, alpha=1.0, bins=50,
    #          histtype='step', edgecolor='orange', linewidth=2.5, label="review modification")
    dates = [r['tcdate'] / 1000 for sub in reviews.values() for r in sub if
             'rating' not in r['content'] and 'abstract' not in r['content']]
    times = mdates.epoch2num([d for d in dates])
    plt.hist(times, normed=False, alpha=1.0, bins=50,
             histtype='step',
             # edgecolor='#ff7272',
             edgecolor='grey',
             linewidth=2.5, label="comments")
    dates = [r['tcdate'] / 1000 for sub in reviews.values() for r in sub if 'rating' in r['content']]
    times = mdates.epoch2num([d for d in dates])
    plt.hist(times, normed=False, alpha=1.0, bins=50,
             histtype='step',
             edgecolor='#ff7272',
             # edgecolor='#f9c51b',
             linewidth=2.5, label="reviews")
    dates = [sub['tcdate'] / 1000 for sub in notes]
    times = mdates.epoch2num([d for d in dates])
    plt.hist(times, normed=False, alpha=1.0, bins=50,
             histtype='step', edgecolor='#44b7ff', linewidth=2.5, label="submission")
    # dates = [sub['tmdate'] / 1000 for sub in notes]
    # times = mdates.epoch2num([d for d in dates])
    # plt.hist(times, normed=False, alpha=1.0, bins=50,
    #          histtype='step', edgecolor='grey', linewidth=2.5, label="modification")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    date_fmt = '%m-%d'  # %H:%M'
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt))
    ax.set_yscale("log", nonposy='clip')
    fig.autofmt_xdate()
    plt.ylabel('# of submissions')
    plt.legend(loc="upper left", framealpha=1, frameon=False)
    plt.savefig(save_prefix + 'submission_timeline.png')
    plt.show()
