import argparse
from data_processor import DataProcessor
from setup import generate_sample_csv

def main():
    parser = argparse.ArgumentParser(description="飞书数据自动化录入工具")
    parser.add_argument(
        '--output',
        choices=['feishu'],
        default='feishu',
        help="输出目标（目前仅支持飞书）"
    )
    generate_sample_csv()
    args = parser.parse_args()
    processor = DataProcessor()
    processor.run_pipeline(args.output)

main()