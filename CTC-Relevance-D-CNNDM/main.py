import argparse, json
import ctc_score

from ctc_score import SummarizationScorer
from ctc_score.configs import TASKS, ALIGNS

parser = argparse.ArgumentParser()
parser.add_argument('--src', help='a file with all documents, line-by-line')
parser.add_argument('--hypo', required=True,
                    help='a file with all hypothesized texts to evaluate, '
                             'line-by-line')
parser.add_argument(
    '--refs',
    help='a file with all references, line-by-line. '
            'if each document has more than one reference, '
            'divide them by \"|||\"')
parser.add_argument('--outfile', type=str, metavar='N',
                    help='output file')
parser.add_argument('--remove_stopwords',
                        default=False, action='store_true',
                        help='whether to remove stopwords in aligning')
args = parser.parse_args()

def read_jsonl(infile, extract_key=None):
    f = open(infile, 'r')
    if extract_key is None:
        out = [json.loads(line.strip()) for line in f]
    else:
        out = [json.loads(line.strip())[extract_key] for line in f]
    f.close()
    return out

def scoring(src, hyp, refs, outfile):
    scorer = SummarizationScorer(align='D-cnndm')
    src = read_jsonl(src, 'src')
    hyp = read_jsonl(hyp, 'hyp')
    refs = read_jsonl(refs, 'refs')
    scores = []

    # relvevance
    for src_s, hyp_s, refs_s in zip(src, hyp, refs):
        scores.append(scorer.score(doc=src_s, refs=refs_s, hypo=hyp_s, aspect='relevance'))
    with open(outfile, 'wt') as fout:
        for score in scores:
            fout.write(str(score))
            fout.write('\n')


if __name__ == '__main__':
    scoring(args.src, args.hypo, args.refs, args.outfile)
