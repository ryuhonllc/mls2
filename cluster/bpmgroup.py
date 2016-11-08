#!/usr/bin/env python


# from scipy.cluster.vq import kmeans, whiten, vq
from scipy.cluster.vq import kmeans, vq
import numpy as np
import re
import argparse


parser = argparse.ArgumentParser(
    description='group songs by bpm using k-means')
parser.add_argument('songfile', type=str,
                    help='filename to be parsed for song names and bpms')
parser.add_argument('-r', '--rubber', action="store_true",
                    help='format output for bpmrubber.rb')
parser.add_argument('-k', '--nclusters', dest='nClusters', type=int,
                    default=3,
                    help='the number of clusters for k-means')

args = parser.parse_args()

fd = open(args.songfile)

pat = re.compile(":?( already tagged,)? ?([0-9.]+)\s+BPM")
comment = re.compile("^\s*#.*")


class Track(object):

    def __init__(self, title, bpm):
        self.title = title.strip()
        self.orig_bpm = bpm
        self.gid = 0
        self.error = 0
        self.new_bpm = bpm

    def __str__(self):
        return "%7.3f %7.3f %5.2f  %s" % (self.orig_bpm, self.new_bpm, self.error, self.title)


tracks = []
bpms = []
for line in fd:
    if comment.match(line):
        continue
    md = pat.search(line)
    if md:
        bpm = md.group(2)
        bpm = float(bpm)
        title = re.sub(pat, "", line)
        track = Track(title, bpm)
        tracks.append(track)
        bpms.append(bpm)


obs = np.array(bpms).T


cb, error = kmeans(obs, args.nClusters)

codes, dist = vq(obs, cb)

total_error = 0
for i, item in enumerate(tracks):
    bpm = cb[codes[i]]
    tracks[i].new_bpm = bpm
    error = dist[i]
    tracks[i].error = error
    total_error += error

tracks.sort(key=lambda x: x.orig_bpm)

curbpm = 0
for _, track in enumerate(tracks):
    if track.new_bpm != curbpm:
        curbpm = track.new_bpm
        print("")
        if args.rubber:
            print("SET %7.3f" % curbpm)
    if args.rubber:
        print("%7.3f BPM %s" % (track.orig_bpm, track.title))
    else:
        print(track)

if not args.rubber:
    n = len(bpms)
    ae = total_error / n
    me = max([x.error for x in tracks])
    print(("%2d songs total error: %5.2f," +
           "average error: %3.2f max error: %3.2f") % (
        n, total_error, ae, me))
