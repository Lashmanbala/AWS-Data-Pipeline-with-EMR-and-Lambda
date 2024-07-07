import os
from download import download_file
from upload import upload_s3
from util import get_prev_file_name, get_next_file_name, upload_bookmark

def lambda_handler(event, context):
    bucket_name = os.environ.get('BUCKET_NAME')
    file_prefix = os.environ.get('FILE_PREFIX')
    bookmark_file = os.environ.get('BOOKMARK_FILE')
    baseline_file = os.environ.get('BASELINE_FILE')

    while True:
        prev_file_name = get_prev_file_name(bucket_name,file_prefix,bookmark_file,baseline_file)
        next_file_name = get_next_file_name(prev_file_name)

        download_res = download_file(next_file_name)
        if download_res.status_code == 404:
            print(f'Invalid file name or downloads caught up till {prev_file_name}')
            break

        upload_res = upload_s3(bucket_name,f'{file_prefix}/{next_file_name}',download_res.content)
        print(f'File {next_file_name} is succssfully processed')

        upload_bookmark(bucket_name,file_prefix,bookmark_file,next_file_name)

    return upload_res