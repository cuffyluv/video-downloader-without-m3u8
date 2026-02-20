# video-downloader-without-m3u8
본 레포지토리는 m3
# 사용법
1. ffmpeg 설치 및 환경변수 등록
   - https://velog.io/@tjdwjdgus99/ffmpeg-%EC%82%AC%EC%9A%A9%EB%B2%95 참고
2. yq 다운로드 (윈도우에선 winget 사용, 에러 발생 시 구글링해서 본인 환경에 맞게 설치)
    ```bash
    winget install mikefarah.yq
    ```
3. 실행
    ```bash
    python -m venv .vevn
    source .venv/Scripts/activate # Windows
    pip install requests # 기타 라이브러리 필요하면 설치
    source run.sh
    ```
4. 결과 확인
   - `outputs/`에 full mp4 video가 생성되었는지 확인
5. 현재는 단일 영상에 대한 다운로드만 지원: 본인 필요에 따라 자동화 스크립트 구축