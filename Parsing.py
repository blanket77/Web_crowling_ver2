import pandas as pd
import glob

def rename_columns_for_goalkeeping_data(file_path):
    # CSV 파일 읽기
    df = pd.read_csv(file_path)
    
    # 컬럼 이름 설정
    df.columns = [
        "번호", "선수", "포지션", "출전시간", "평점",
        "실점", "캐칭", "펀칭", "골킥성공", "골킥성공률(%)",
        "공중볼처리성공", "공중볼처리성공률(%)", "Ishome"
    ]
    
    # 수정된 데이터 저장
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"Processed file: {file_path}")


def rename_columns_for_attack_data(file_path):
    # CSV 파일을 데이터프레임으로 로드
    df = pd.read_csv(file_path)

    # 열 이름이 '성공'과 '성공률(%)'인 경우에 '드리블 성공'과 '드리블 성공률(%)'로 변경
    df = df.rename(columns={"성공": "드리블 성공", "성공률(%)": "드리블 성공률(%)"})

    # 변경된 데이터프레임을 다시 CSV 파일로 저장 (덮어쓰기)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"Processed file: {file_path}")


def rename_columns_for_defensive_data(file_path):
    # CSV 파일을 데이터프레임으로 로드
    df = pd.read_csv(file_path)

    # 열 이름 변경 (성공, 성공률을 경합(지상)성공 등으로 변경)
    df.columns = [
        "번호", "선수", "포지션", "출전시간", "평점",
        "경합(지상)성공", "경합(지상)성공률(%)",
        "경합(공중)성공", "경합(공중)성공률(%)",
        "태클성공", "태클성공률(%)",
        "클리어링", "인터셉트", "차단", "획득", "블락", "볼미스",
        "파울", "피파울", "경고", "퇴장", "Ishome"
    ]

    # 변경된 데이터프레임을 다시 CSV 파일로 저장 (덮어쓰기)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"Processed file: {file_path}")

def rename_columns_for_passing_data(file_path):
    # CSV 파일을 데이터프레임으로 로드
    df = pd.read_csv(file_path)

    # 열 이름을 새로운 형식으로 변경
    df.columns = [
        "번호", "선수", "포지션", "출전시간", "평점",
        "패스성공", "패스성공률(%)", "키패스",
        "공격진영패스성공", "공격진영패스성공률(%)",
        "중앙지역패스성공", "중앙지역패스성공률(%)",
        "수비진영패스성공", "수비진영패스성공률(%)",
        "롱패스성공", "롱패스성공률(%)",
        "중거리패스성공", "중거리패스성공률(%)",
        "숏패스성공", "숏패스성공률(%)",
        "전진패스성공", "전진패스성공률(%)",
        "횡패스성공", "횡패스성공률(%)",
        "백패스성공", "백패스성공률(%)",
        "크로스성공", "크로스성공률(%)",
        "탈압박" ,"Ishome"
    ]

    # 변경된 데이터프레임을 다시 CSV 파일로 저장 (덮어쓰기)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"Processed file: {file_path}")


if __name__ == '__main__':
    # 파일 이름이 '*골키퍼_data.csv' 패턴에 맞는 모든 CSV 파일을 처리
    csv_files = glob.glob("*골키퍼_data.csv")  # 파일 이름이 '골키퍼_data.csv'로 끝나는 모든 파일을 찾습니다.
    for file_path in csv_files:
        rename_columns_for_goalkeeping_data(file_path)

    # 모든 CSV 파일을 처리
    csv_files = glob.glob("*공격_data.csv")  # 현재 디렉토리 내의 모든 CSV 파일을 찾습니다.
    for file_path in csv_files:
        rename_columns_for_attack_data(file_path)

    # 파일 이름이 '*패스_data.csv' 패턴에 맞는 모든 CSV 파일을 처리
    csv_files = glob.glob("*패스_data.csv")  # 예를 들어 '패스_data.csv'로 끝나는 모든 파일을 찾습니다.
    for file_path in csv_files:
        rename_columns_for_passing_data(file_path)

    # 파일 이름이 '*수비_data.csv' 패턴에 맞는 모든 CSV 파일을 처리
    csv_files = glob.glob("*수비_data.csv")  # 파일 이름이 '수비_data.csv'로 끝나는 모든 파일을 찾습니다.
    for file_path in csv_files:
        rename_columns_for_defensive_data(file_path)