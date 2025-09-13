from scripts.train import recognizer

trn = '../data/train/train.txt'
dev = '../data/train/dev.txt'
save_dir = '../data/model/ner/product'
transformer = 'bert-base-chinese'

for bs in [8, 16, 32, 64]:
    try:
        recognizer.fit(
            trn_data=trn,
            dev_data=dev,
            save_dir=save_dir,
            transformer=transformer,
            batch_size=bs
        )
    except RuntimeError:
        print(f"batch_size={bs} 太大，顯存不足")