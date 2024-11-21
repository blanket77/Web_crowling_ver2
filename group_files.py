import pandas as pd
import glob
import os
from globals import GO_YEAR
import shutil

# 파일을 그룹화하는 함수
def group_files_by_prefix(data_directory, file_pattern):
    """
    지정된 패턴에 맞는 파일들을 그룹화하여 반환하는 함수.

    :param data_directory: 검색할 디렉토리 경로
    :param file_pattern: 검색할 파일 이름 패턴
    :return: 접두사로 그룹화된 파일 딕셔너리
    """
    # 지정된 패턴에 맞는 파일들을 검색
    file_patterns = glob.glob(os.path.join(data_directory, file_pattern))
    
    # 접두사로 파일을 그룹화
    file_groups = {}
    for file in file_patterns:
        prefix = file.split('/')[-1].split(')')[0] + ')'
        
        if prefix not in file_groups:
            file_groups[prefix] = []
        file_groups[prefix].append(file)
    
    return file_groups

# 데이터를 로드하고 병합하는 함수
def load_and_concatenate(file_list):
    """
    passMatrix 파일을 제외하고 CSV 파일을 로드하고 병합하는 함수.

    :param file_list: 병합할 파일들의 목록
    :return: 병합된 데이터프레임 목록
    """
    dataframes = []
    for file in file_list:
        if "passMatrix" not in file and "골키퍼" not in file:  # passMatrix 파일 제외
            df = pd.read_csv(file)
            dataframes.append(df)
    return dataframes  # List of DataFrames, do not concatenate yet

# 데이터를 병합하고 저장하는 함수
def merge_and_save_data(data_directory, file_groups):
    """
    파일 그룹에 대해 데이터를 병합하고 저장하는 함수.

    :param data_directory: 저장할 디렉토리 경로
    :param file_groups: 접두사로 그룹화된 파일들
    """
    for prefix, files in file_groups.items():
        dfs = load_and_concatenate(files)  # 데이터 로드
        
        if dfs:
            # 첫 번째 데이터프레임으로 초기화
            combined_df = dfs[0]
            
            # 나머지 데이터프레임을 '선수' 기준으로 병합
            for df in dfs[1:]:
                combined_df = pd.merge(combined_df, df, on='선수', how='outer', suffixes=('', '_drop'))

                # 중복된 열 제거
                combined_df = combined_df.loc[:, ~combined_df.columns.str.endswith('_drop')]

            # 결측값을 0으로 채우기
            combined_df.fillna(0, inplace=True)

            # 최종 데이터프레임을 저장
            output_filename = os.path.join(data_directory + "together/", f"{prefix}모두_data.csv")
            combined_df.to_csv(output_filename, index=False)

            # 결과 출력
            print(f"Data saved as: {output_filename}")

####################passmatrix끼리 따로 폴더 ########################


def copy_pass_matrix_files(source_dir='./', destination_dir=None):
    """
    source_dir에서 'passMatrix'가 포함된 파일을 찾아서 destination_dir로 복사하는 함수.

    :param source_dir: 검색할 폴더 경로 (기본값은 현재 폴더)
    :param destination_dir: 파일을 복사할 대상 폴더 경로. GO_YEAR을 사용해 경로를 설정
    """
    # destination_dir이 None이면 기본값 설정
    if destination_dir is None:
        destination_dir = './' + str(GO_YEAR) + '_passMatrix'

    # 대상 폴더가 없으면 새로 생성
    os.makedirs(destination_dir, exist_ok=True)

    # source_dir에서 파일명에 'passMatrix'가 포함된 파일을 찾고, 대상 폴더로 복사
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if 'passMatrix' in file:
                # 파일 경로 설정
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_dir, file)
                
                # 파일이 서로 다른 경우에만 복사
                if os.path.abspath(source_file) != os.path.abspath(destination_file):
                    shutil.copy2(source_file, destination_file)
                    print(f"파일 복사됨: {file}")
                else:
                    print(f"같은 파일이라 복사하지 않음: {file}")


####################goalkeeper끼리 따로 폴더 ########################
def copy_files_with_pattern(source_dir, destination_dir, pattern):
    """
    source_dir에서 특정 패턴이 포함된 파일을 찾아 destination_dir로 복사하는 함수.

    :param source_dir: 검색할 폴더 경로
    :param destination_dir: 파일을 복사할 대상 폴더 경로
    :param pattern: 파일명에 포함될 패턴
    """
    # 대상 폴더가 없으면 새로 생성
    os.makedirs(destination_dir, exist_ok=True)

    # source_dir에서 파일명에 패턴이 포함된 파일을 찾고, 대상 폴더로 복사
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if pattern in file:
                # 파일 경로 설정
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_dir, file)

                # 파일이 서로 다른 경우에만 복사
                if os.path.abspath(source_file) != os.path.abspath(destination_file):
                    shutil.copy2(source_file, destination_file)
                    print(f"파일 복사됨: {file}")
                else:
                    print(f"같은 파일이라 복사하지 않음: {file}")


# 사용 예시
def main():
    data_directory = './'  # 데이터 디렉토리 경로
    file_pattern = str(GO_YEAR) + '*'  # 파일 검색 패턴
    
    # 파일 그룹화
    file_groups = group_files_by_prefix(data_directory, file_pattern)
    
    # 데이터 병합 및 저장
    merge_and_save_data(data_directory, file_groups)

    copy_pass_matrix_files()  # matrix 파일을 다른 폴더로 복사

    source_dir = './'  # 검색할 폴더 경로
    destination_dir = './'+ str(GO_YEAR) +'_골키퍼'  # 파일을 복사할 대상 폴더 경로
    pattern = '골키퍼_'  # 파일명에 포함된 패턴

    copy_files_with_pattern(source_dir, destination_dir, pattern)


# 메인 함수 실행
if __name__ == '__main__':
    main()
