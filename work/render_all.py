#!/usr/bin/env python3
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_video import (compose_photo_frame, compose_text_frame, compose_twocol_frame,
                          compose_number_frame, render_clip, FRAMES, CLIPS, ROOT)
from edl import EDL, TOTAL_DURATION

def fill_gaps(edl, total):
    out = []
    cursor = 0.0
    for (s, e, kind, payload) in edl:
        if s - cursor > 0.02:
            out.append((cursor, s, 'dark', None))
        out.append((s, e, kind, payload))
        cursor = e
    if total - cursor > 0.02:
        out.append((cursor, total, 'dark', None))
    return out

def main():
    full = fill_gaps(EDL, TOTAL_DURATION)
    text_card_cache = {}
    clip_list = []
    for idx, (s, e, kind, payload) in enumerate(full):
        dur = e - s
        png = os.path.join(FRAMES, f'{idx:04d}_{kind}.jpg')
        zoom = True
        if kind == 'photo':
            compose_photo_frame(payload, png)
        elif kind == 'text':
            key = ('text', tuple(payload))
            if key not in text_card_cache:
                compose_text_frame(png, payload)
                text_card_cache[key] = png
            else:
                png = text_card_cache[key]
            zoom = False
        elif kind == 'twocol':
            key = ('twocol',)
            if key not in text_card_cache:
                compose_twocol_frame(png)
                text_card_cache[key] = png
            else:
                png = text_card_cache[key]
            zoom = False
        elif kind == 'number':
            compose_number_frame(png, payload)
            zoom = False
        elif kind == 'dark':
            key = ('dark',)
            if key not in text_card_cache:
                compose_text_frame(png, [], bg=(12, 12, 12))
                text_card_cache[key] = png
            else:
                png = text_card_cache[key]
            zoom = False
        else:
            raise ValueError(kind)

        clip_mp4 = os.path.join(CLIPS, f'{idx:04d}.mp4')
        render_clip(png, dur, clip_mp4, zoom=zoom)
        clip_list.append(clip_mp4)
        print(f'[{idx+1}/{len(full)}] {kind:6s} {s:7.2f}-{e:7.2f} ({dur:5.2f}s) -> {os.path.basename(clip_mp4)}')

    concat_file = os.path.join(ROOT, 'work', 'concat.txt')
    with open(concat_file, 'w') as f:
        for c in clip_list:
            f.write(f"file '{c}'\n")

    video_only = os.path.join(ROOT, 'work', 'video_only.mp4')
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_file,
                     '-c', 'copy', video_only], check=True)

    audio = os.path.join(ROOT, 'audio', 'voix_off_finale.wav')
    out_final = os.path.join(ROOT, 'output', 'bref_cremaillere_v1.mp4')
    subprocess.run(['ffmpeg', '-y', '-i', video_only, '-i', audio,
                     '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                     '-shortest', out_final], check=True)
    print('DONE ->', out_final)

if __name__ == '__main__':
    main()
