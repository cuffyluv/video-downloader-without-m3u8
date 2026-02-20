# video-downloader-without-m3u8
본 레포지토리는 m3u8을 노출하지 않는 HLS video에 대해 ts file의 request_url로부터 패턴을 추정해 video를 concat하는 downloader입니다.  
암호화된 segment에 대한 복호화는 지원하지 않습니다.

## Disclaimer
<h3 align="center">
    🚨 본 레포지토리는 MIT License by cuffyluv를 따르며, 레포지토리 개발자는 본 레포지토리를 활용한 어떠한 행위에 대해서도 법적으로 보증하지 않습니다!!
</h3>
<h3 align="center">
    🚨 본 레포지토리를 활용해 download가 금지된 저작권이 있는 영상을 다운로드한다면, 법적 책임을 물 수 있습니다!! 시도하지 마시길 바랍니다.
</h3>
<h3 align="center">
    🚨 본 레포지토리에서는 자세한 url request 및 signed query 방법에 대해서는 설명하지 않고 있으며, 사용자가 이를 직접 알아내도록 지시하고 있습니다.
</h3>
<h3 align="center">
    🚨 CC 계열 license 중 download 및 개인 소장에 자유로은 license video에 대해, 영상 소유주에게 사전 고지 후 download를 시도하시길 권고드립니다.
</h3>


## 시작 전에, 만약 m3u8 file을 어떻게든 구해냈다면?
축하드립니다. 어떤 방법을 쓰셨든간에에 m3u8 file을 구하셨다면, 아래의 행위들을 하실 필요가 전혀 없습니다.  
아래 과정들이 과정들이 전부 "m3u8(=.ts의 playlist)가 없으니까, m3u8을 흉내내는 playlist txt file을 만들어보자!"는 목적으로 진행되고 있기 때문에, m3u8 file이 존재하신다면 전부 skip하셔도 됩니다.  
이 경우 ffmpeg를 이용하셔도 되고, yt-dlp와 같은 시중의 프로그램을 사용하셔도 됩니다. 구글링을 하셔도 정보가 많이 나오실 거고요.
예시를 들어드리자면 다음과 같을 것 같고요(둘다 병렬 버전 기준):
```bash
# ffmpeg 사용
ffmpeg -http_seekable 0 -http_persistent 1 -threads 0 -i "https://path/to/your/m3u8/file.m3u8" -c copy video.mp4
# yt-dlp 사용
yt-dlp --concurrent-fragments 16 "https://path/to/your/m3u8/file.m3u8" -o "video.mp4"
```
참고로 로그인이 필요한 동영상이어서 cookie 사용이 필요하면 yt-dlp를 사용하셔도 되는데, 그게 아니라면 굳이 사용하실 필요는 없습니다. 순정 ffmpeg가 더 나을 거에요.

하지만, **그 어떠한한 방법을 써 봐도, m3u8 file을 찾을 수 없다면!!** 그렇다면 최후의 방법으로 이 레포지토리를 참고하셔서 파이썬 스크립트를 직접 짜시는 것 밖에는 방법이 없을 겁니다.  
(왜냐하면 제가 온갖 방법을 다 써보고 다 실패했거든요. 만약 더 나은 방법이 있다면 알려주세요.)


## 개발한 이유 및 필요성
보통 시중의 HLS video downloader는 Network의 .ts file들의 목록이 m3u8 file에 적혀서 우리에게 전송될 것이라고 기대하고, 해당 m3u8 file을 읽어서 .ts file들을 download 및 concat하는 식으로 구현됩니다.  
그러나 일부 video들은 m3u8을 숨기고 오직 .ts file들만을 제공하기도 합니다.

즉 이런 경우는 m3u8 file 자체가 없으므로, 당연히 시중의 HLS video downloader을 사용할 수 없고,  
직접 python이든 javascript든 스크립트를 짜서 .ts file을 일일이 다운받는 과정이 필요합니다.

그러나 m3u8 file은 숨겨져 있지만 .ts file들의 request_url이 특정 패턴을 보이는 경우,  
**우리는 해당 패턴을 가지고 m3u8 file 또는 그와 같은 역할을 하는 .txt file을 역으로 유추, 생성할 수 있습니다!!**  

본 레포지토리에서는 우리가 yaml file로 입력한 그 pattern에 맞춰 m3u8 file의 대용으로 filelist.txt을 생성하고,  
해당 파일 내용으로 ffmpeg를 사용해 .ts file들을 concat하는 일련의 과정을  
python 및 shell script로 구현하였습니다.

## 사용법
1. ffmpeg 설치 및 환경변수 등록
   - https://velog.io/@tjdwjdgus99/ffmpeg-%EC%82%AC%EC%9A%A9%EB%B2%95 참고
2. yq 다운로드 (윈도우에선 winget 사용, 에러 발생 시 구글링해서 본인 환경에 맞게 설치)
    ```bash
    winget install mikefarah.yq
    ```
3. 본인이 다운로드하고자 하는 video에 맞춰서 .yaml config file을 수정
   - 각 인자에 대한 설명은 생략하겠음. 필요하다면 문의 주시거나 직접 파악해 보시기를 추천드립니다.
4. 실행
    ```bash
    python -m venv .vevn
    source .venv/Scripts/activate # Windows
    pip install requests # 기타 라이브러리 필요하면 설치
    source run.sh
    ```
5. 결과 확인
   - `outputs/`에 full mp4 video가 생성되었는지 확인
6. 현재는 단일 영상에 대한 다운로드만 지원: 본인 필요에 따라 자동화 스크립트 구축