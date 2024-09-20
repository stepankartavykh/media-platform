import json
import os


# from DataApp.config import LOCAL_STORAGE_PATH


class DataPacket:
    pass


def process_data_packet(data_packet: dict) -> DataPacket:
    keys = list(data_packet.keys())
    if 'status' in keys:
        packets = data_packet.get('articles')
        if packets:
            for pack in packets:
                print(pack)
    else:
        raise Exception('Something wrong with data_packet')
    return DataPacket()


def load(directory_path: str):
    for file in os.listdir(directory_path):
        if not file.endswith('json'):
            continue
        file_path = os.path.join(directory_path, file)
        if os.path.isdir(file_path):
            print(file_path, '- directory')
            continue
        articles_from_file = []
        try:
            with open(file_path, 'r') as file_reader:
                data = json.load(file_reader)
            if isinstance(data, list):
                for data_packet in data:
                    try:
                        process_data_packet(data_packet)
                    except Exception:
                        print('file:', file)
                        raise
            elif isinstance(data, dict):
                if data.get('status') not in ('ok', 'success'):
                    print(f'smth wrong with file {file}')
                    print(data.keys())
                    continue
        except json.decoder.JSONDecodeError as json_error:
            print(json_error)
            print('error in file', file)


if __name__ == '__main__':
    LOCAL_STORAGE_PATH = '/home/skartavykh/MyProjects/media-bot/storage'
    load(LOCAL_STORAGE_PATH)
