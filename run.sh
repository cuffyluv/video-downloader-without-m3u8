#!/bin/bash
# run.sh

CONFIG="configs/example_for_upload.yaml"

if [ ! -f "$CONFIG" ]; then
    echo "yaml 파일이 없습니다."
    exit 1
fi

BASE_URL=$(yq e '.video.base_url' "$CONFIG")
SIGNED_QUERY=$(yq e '.video.signed_query' "$CONFIG")
OUT_DIR=$(yq e '.video.output_dir' "$CONFIG")
MAX_SEG=$(yq e '.video.max_segments' "$CONFIG")
WORKERS=$(yq e '.video.workers' "$CONFIG")
VIDEO_NAME=$(yq e '.video.video_name' "$CONFIG")

if [ -z "$VIDEO_NAME" ]; then
    VIDEO_NAME="temp.mp4"
fi

echo "=== 설정 ==="
echo "output_dir   : $OUT_DIR"
echo "video_name   : $VIDEO_NAME"
echo "============="

python advanced_download_ts.py \
    --base-url "$BASE_URL" \
    --signed-query "$SIGNED_QUERY" \
    --output-dir "$OUT_DIR" \
    --max-segments "$MAX_SEG" \
    --workers "$WORKERS"

if [ $? -ne 0 ]; then
    echo "다운로드 실패"
    exit 1
fi

echo "다운로드 완료. 합치기 시작..."

# cd 해서 상대 경로로 처리 (이게 제일 안정적)
pushd "$OUT_DIR" > /dev/null || { echo "cd $OUT_DIR 실패"; exit 1; }

# 상대 경로로 filelist.txt 생성
ls -1 seg_*.ts 2>/dev/null | sort -V | awk '{print "file \047" $0 "\047"}' > filelist.txt

if [ ! -s filelist.txt ]; then
    echo "seg_*.ts 파일 없음"
    popd > /dev/null
    exit 1
fi

echo "총 $(wc -l < filelist.txt)개 세그먼트"

# ffmpeg 실행 (상대 경로로)
ffmpeg -f concat -safe 0 -i filelist.txt -c copy "$VIDEO_NAME" || {
    echo "ffmpeg 실패 (코드 $?)"
    rm -f filelist.txt
    popd > /dev/null
    exit 1
}

# 정리
rm -f filelist.txt

# 원본 ts들 삭제
rm seg*
echo "원본 seg들 삭제!"

popd > /dev/null

echo "합치기 완료! 결과: $OUT_DIR/$VIDEO_NAME"