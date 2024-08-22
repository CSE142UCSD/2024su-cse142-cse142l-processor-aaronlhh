#!/usr/bin/env python

import click
import os
import json
import re
#from csvtools import qcsv
#from CSE142L.jextract import extract as qjson
#from notebook import render_csv
import pandas as pd

        
def compute_scores(df, FOM, targets):
    (base_FOM, target_S) = zip(*targets)
    
    df = df.copy()
    baseFOM='reference'+"_"+FOM
    df = df.loc[(df["function"] == "select_case_solution_c")].copy().reset_index()
    df['target_speedup'] = target_S
    df[baseFOM] = base_FOM
    df['speedup'] = df[baseFOM]/df[FOM]
    df['bench_score'] = df['speedup']/df['target_speedup'] * 100.0
    
    return df[['label',
               'orders',
               'target_speedup', baseFOM, FOM, 'speedup', 'bench_score']]

def compute_correctness(dir=None):
    if dir == None:
        dir=""

    def csv(f):
        return pd.read_csv(f, sep=",")

    results = csv(os.path.join(dir, "correctness.csv"))

    corrects = results["correctness"].sum()
    return corrects

def compute_all_scores(dir=None):
    if dir == None:
        dir=""

    def csv(f):
        return pd.read_csv(f, sep=",")

    bench = csv(os.path.join(dir, "bench.csv"))

    bench["label"] = bench["function"] + " " + list(map(str,bench["customers"]))
    #                                     baseline ET     Speedup
    # scores = compute_scores(bench, "ET",[(3.19,2.2),
    #                                      (7.52,3.5),
    #                                      (2.9,18.5)])
    scores = compute_scores(bench, "ET",[(17.8,2.5)])
    
    scores['score'] = round(scores['bench_score']/len(scores),2)
    scores['capped_score'] = list(map(lambda x: min(100.0/len(scores), x), scores['score']))
    
    return scores.copy()
    

@click.command()
@click.option("--submission", required=True,  type=click.Path(exists=True), help="Test directory")
@click.option("--results", required=True, type = click.File(mode="w"), help="Where to put results")
def autograde(submission=None, results=None):
    try:
        failures = 6 - compute_correctness(dir=submission)
        output = "tests passed" if failures == 0 else "Your code is incorrect"
    except FileNotFoundError as e:
        output = f"I couldn't find your regression outputs.  This often means your program generated a segfault :{e}."
        failures = 1
    except Exception as e:
        output = f"I got an unexpected exception processing the regressions.  Tell the course staff:{e}."
        failures = 1
    finally:
        regressions = dict(score=1 if failures == 0 else 0,
                           max_score=1,
                           number="1",
                           output=output,
                           tags=[],
                           visibility="visible")
        
    benchmarks = []
    leaderboard=[]
    try:
        scores  = compute_all_scores(dir=submission)
    except FileNotFoundError as e:
        benchmarks.append(dict(score=0,
                               max_score=100,
                               output = f"I couldn't find a csv file.  This often means your program generated a segfault or failed the regressions :{e}.",
                               tags=(),
                               visibility="visible"))
    except Exception as e:
        benchmarks.append(dict(score=0,
                               max_score=100,
                               output = f"I got an unexpected exception evaluating the benchmarks.  Tell the course staff.:{e}.",
                               tags=(),
                               visibility="visible"))
    else:
        count = len(scores)
        for index, row in scores.iterrows():
            benchmarks.append(dict(score=round(row['capped_score'],2) if failures == 0 else 0,
                    max_score=100.0/count,
                    output=f"Test: {row['label']}:  The target speedup is {row['target_speedup']:2.2f}x, your speedup is {row['speedup']:2.2f}x.  Your score is {row['speedup']:2.2f}/{row['target_speedup']}*{100.0/count:2.2f} = {row['score']:2.2f} (or {100.0/count}, if that values is greater than {100.0/count})" if failures == 0 else "Your code is incorrect, so speedup is meaningless.",
                    tags=[],
                    visibility="visible"))

        leaderboard = []
        for index, row in scores.iterrows():
            leaderboard.append(dict(name=row['label'] + " speedup", value=round(row['speedup'],2)))

    if os.path.exists("/autograder/results/stdout"):
        with open("/autograder/results/stdout") as f:
            stdout = f.read()
    else:
        stdout = ""
        
    # https://gradescope-autograders.readthedocs.io/en/latest/specs/#output-format
    json.dump(dict(output=stdout,
                   visibility="visible",
                   stdout_visibility="visible",
                   tests=benchmarks,
                   leaderboard=leaderboard
        ), results, indent=4)
        
if __name__== "__main__":
    autograde()
