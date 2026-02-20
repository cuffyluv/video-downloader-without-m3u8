# advanced_download_ts.py
import requests
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

def parse_args():
    parser = argparse.ArgumentParser(description="video-downloader-without-m3u8")
    parser.add_argument("--base-url", required=True, help="세그먼트 기본 URL (마지막 -000000.ts 전까지)")
    parser.add_argument("--signed-query", required=True, help=".ts 다음 부분")
    parser.add_argument("--output-dir", default="segments", help="세그먼트 저장 폴더 (기본: segments)")
    parser.add_argument("--max-segments", type=int, default=2000, help="최대 시도할 세그먼트 수")
    parser.add_argument("--workers", type=int, default=8, help="동시 다운로드 스레드 수")
    parser.add_argument("--dry-run", action="store_true", help="실제 다운로드 없이 URL만 출력")
    return parser.parse_args()

def main():
    args = parse_args()

    # 출력 폴더 생성
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    base_url = args.base_url.rstrip('-')  # 끝에 -가 붙어있을 수 있으니 정리
    if not base_url.endswith('-'):
        base_url += '-'

    signed_query = args.signed_query
    if not signed_query.startswith('?'):
        signed_query = '?' + signed_query

    print(f"설정:")
    print(f"  base_url     : {base_url}")
    print(f"  signed_query : {signed_query}")
    print(f"  output_dir   : {output_path.absolute()}")
    print(f"  max_segments : {args.max_segments}")
    print(f"  workers      : {args.workers}\n")

    def download_segment(n):
        num_str = f"{n:06d}"
        url = f"{base_url}{num_str}.ts{signed_query}"
        filename = output_path / f"seg_{num_str}.ts"

        if filename.exists():
            print(f"이미 존재: {filename}")
            return True

        if args.dry_run:
            print(f"[DRY] {url}")
            return True

        try:
            r = requests.get(url, timeout=20, stream=True)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                size_mb = filename.stat().st_size / (1024 * 1024)
                print(f"다운로드 완료: {filename} ({size_mb:.2f} MB)")
                return True
            else:
                print(f"중단 ({n}): HTTP {r.status_code}")
                return False
        except Exception as e:
            print(f"에러 ({n}): {e}")
            return False

    success_count = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(download_segment, i) for i in range(args.max_segments)]
        for future in futures:
            if future.result():
                success_count += 1
            else:
                break  # 실패하면 중단

    print(f"\n완료! 총 {success_count}개 세그먼트 다운로드")

if __name__ == "__main__":
    main()