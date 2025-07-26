from flask import Flask, request, render_template, jsonify
import cudf
import pandas as pd
import json
import logging
import time
import psutil

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Load the entire JSON file into a pandas DataFrame once at startup
def load_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df = df.astype(str)
    return df

JSON_FILE_PATH = 'steamdb.json'
pdf = load_json(JSON_FILE_PATH)  # Pandas DataFrame
df = cudf.DataFrame.from_pandas(pdf)  # cuDF DataFrame

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    query_string = request.form.get('query')
    match_all = request.form.get('match_all') == 'on'
    logging.debug(f"Received query: {query_string}, match_all: {match_all}")

    if not query_string:
        return render_template('index.html', error="No query provided")

    start = int(request.form.get('start', 0))
    limit = int(request.form.get('limit', 50))

    # cuDF query
    start_time = time.time()
    memory_before = psutil.Process().memory_info().rss

    try:
        queries = [q.strip() for q in query_string.split(';')]
        if match_all:
            result_df = df
            for q in queries:
                if '==' in q:
                    col, value = q.split('==')
                    col, value = col.strip(), value.strip().strip('"').strip("'")
                    if col in ['achievements', 'current_price']:
                        result_df = result_df[result_df[col] == int(value)]
                    elif col in ['gfq_rating']:
                        result_df = result_df[result_df[col] == float(value)]
                    else:
                        result_df = result_df[result_df[col].str.lower() == value.lower()]
                else:
                    raise ValueError("Unsupported query format")
        else:
            result_df = cudf.concat([
                df[df[col.strip()].str.lower() == value.strip().strip('"').strip("'").lower()]
                for query in queries if '==' in query
                for col, value in [query.split('==')]
            ])

        total_results = len(result_df)
        result_df = result_df[start:start+limit]
        result = result_df.drop_duplicates().to_pandas().to_dict(orient='records')
        logging.debug(f"Query result: {result}")

        memory_after = psutil.Process().memory_info().rss
        end_time = time.time()

        cudf_query_time = end_time - start_time
        cudf_memory_usage = (memory_after - memory_before) / 1024 / 1024  # Convert to MB

        # Pandas query for comparison
        start_time = time.time()

        if match_all:
            result_pdf = pdf
            for q in queries:
                if '==' in q:
                    col, value = q.split('==')
                    col, value = col.strip(), value.strip().strip('"').strip("'")
                    if col in ['achievements', 'current_price']:
                        result_pdf = result_pdf[result_pdf[col] == int(value)]
                    elif col in ['gfq_rating']:
                        result_pdf = result_pdf[result_pdf[col] == float(value)]
                    else:
                        result_pdf = result_pdf[result_pdf[col].str.lower() == value.lower()]
                else:
                    raise ValueError("Unsupported query format")
        else:
            result_pdf = pd.concat([
                pdf[pdf[col.strip()].str.lower() == value.strip().strip('"').strip("'").lower()]
                for query in queries if '==' in query
                for col, value in [query.split('==')]
            ])

        pandas_query_time = time.time() - start_time

        if result:
            return render_template('index.html', results=result, query=query_string, total_results=total_results, start=start, limit=limit, total_games=len(df),
                                   cudf_query_time=cudf_query_time, cudf_memory_usage=cudf_memory_usage, pandas_query_time=pandas_query_time)
        else:
            return render_template('index.html', error="No results found.", query=query_string, total_results=total_results, start=start, limit=limit, total_games=len(df),
                                   cudf_query_time=cudf_query_time, cudf_memory_usage=cudf_memory_usage, pandas_query_time=pandas_query_time)

    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return render_template('index.html', error=str(e), query=query_string, total_results=0, start=start, limit=limit, total_games=len(df), cudf_query_time=0, cudf_memory_usage=0, pandas_query_time=0)

@app.route('/load_more', methods=['POST'])
def load_more():
    query_string = request.form.get('query')
    start = int(request.form.get('start', 0))
    limit = int(request.form.get('limit', 50))
    match_all = request.form.get('match_all') == 'on'

    start_time = time.time()
    memory_before = psutil.Process().memory_info().rss

    try:
        queries = [q.strip() for q in query_string.split(';')]
        if match_all:
            result_df = df
            for q in queries:
                if '==' in q:
                    col, value = q.split('==')
                    col, value = col.strip(), value.strip().strip('"').strip("'")
                    if col in ['achievements', 'current_price']:
                        result_df = result_df[result_df[col] == int(value)]
                    elif col in ['gfq_rating']:
                        result_df = result_df[result_df[col] == float(value)]
                    else:
                        result_df = result_df[result_df[col].str.lower() == value.lower()]
                else:
                    raise ValueError("Unsupported query format")
        else:
            result_df = cudf.concat([
                df[df[col.strip()].str.lower() == value.strip().strip('"').strip("'").lower()]
                for query in queries if '==' in query
                for col, value in [query.split('==')]
            ])

        total_results = len(result_df)
        result_df = result_df[start:start+limit]
        result = result_df.drop_duplicates().to_pandas().to_dict(orient='records')
        logging.debug(f"Load more result: {result}")

        memory_after = psutil.Process().memory_info().rss
        end_time = time.time()

        cudf_query_time = end_time - start_time
        cudf_memory_usage = (memory_after - memory_before) / 1024 / 1024  # Convert to MB

        return jsonify(results=result, total_results=total_results, start=start + limit, cudf_query_time=cudf_query_time, cudf_memory_usage=cudf_memory_usage)

    except Exception as e:
        logging.error(f"Error executing load more: {e}")
        return jsonify(error=str(e))

@app.route('/game/<int:sid>')
def game_details(sid):
    try:
        game = df[df['sid'] == str(sid)].to_pandas().to_dict(orient='records')
        if not game:
            raise ValueError("Game not found")
        game = game[0]
        # Convert the current_price and full_price to integers
        game['current_price'] = int(float(game['current_price']))
        if 'full_price' in game and game['full_price']:
            game['full_price'] = int(float(game['full_price']))
        return render_template('game.html', game=game)
    except Exception as e:
        logging.error(f"Error fetching game details: {e}")
        return render_template('game.html', error="Game not found")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
