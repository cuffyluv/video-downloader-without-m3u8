# video-downloader-without-m3u8
본 레포지토리는 m3u8을 노출하지 않는 HLS video에 대해 ts file의 request_url로부터 패턴을 추정해 video를 concat하는 downloader입니다.  
암호화된 segment에 대한 복호화는 지원하지 않습니다.

## Disclaimer
<h3 align="center">
    🚨 본 레포지토리는 MIT License by cuffyluv를 따르며, 개발자 cuffyluv는 본 레포지토리를 활용한 어떠한 행위에 대해서도 법적으로 보증하지 않습니다!!
</h3>
<h3 align="center">
    🚨 본 레포지토리를 활용해 download가 금지된 저작권이 있는 영상을 다운로드한다면, 법적 책임을 물 수 있습니다!! 시도하지 마시길 바랍니다.
</h3>
<h3 align="center">
    🚨 본 레포지토리에서는 자세한 url parsing 방법에 대해서는 설명하지 않고 있으며, 사용자가 이를 직접 알아내도록 지도하고 있습니다.
</h3>
<h3 align="center">
    🚨 CC 계열 license 중 download 및 개인 소장에 자유로은 license video에 대해, 영상 소유주에게 사전 고지 후 download를 시도하시길 권고드립니다.
</h3>

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