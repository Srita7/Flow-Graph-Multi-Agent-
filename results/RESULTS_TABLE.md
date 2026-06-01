# Evaluation Results: Combined Tables

- **Table 1 (Baseline):** 5 libraries, 55 programs with metrics; — for ansible, black, luigi, scrapy, tornado.
- **Table 2:** COT_TOT_C and COT_TOT_PYTHON (TOT) — 10 libraries, 100 programs.
- **Table 3 (C):** Columns **graph_based_LD**, **english_cot_tot**, **graph_based_cos_sim**, **english_tot_cot** (graph_based = TOT, english = COT from COT_TOT_C).
- **Table 4 (Python):** Same four columns (graph_based = baseline from results/; english = COT and TOT from COT_TOT_PYTHON).

---

# Table 1: Baseline (results/) — 5 libraries, 55 programs with metrics; — for ansible, black, luigi, scrapy, tornado

| # | Library | Program | Baseline Levenshtein | Baseline Cosine |
|---|---------|---------|----------------------|-----------------|
| 1 | ansible | bug1.py | — | — |
| 2 | ansible | bug2.py | — | — |
| 3 | ansible | bug3.py | — | — |
| 4 | ansible | bug4.py | — | — |
| 5 | ansible | bug5.py | — | — |
| 6 | ansible | bug6.py | — | — |
| 7 | ansible | bug7.py | — | — |
| 8 | ansible | bug8.py | — | — |
| 9 | ansible | bug9.py | — | — |
| 10 | black | bug1.py | — | — |
| 11 | black | bug2.py | — | — |
| 12 | black | bug3.py | — | — |
| 13 | black | bug4.py | — | — |
| 14 | black | bug5.py | — | — |
| 15 | black | bug6.py | — | — |
| 16 | black | bug7.py | — | — |
| 17 | black | bug8.py | — | — |
| 18 | black | bug9.py | — | — |
| 19 | fastapi | bug1.py | 60 | 0.9994 |
| 20 | fastapi | bug2.py | 8 | 0.9594 |
| 21 | fastapi | bug5.py | 3 | 0.9934 |
| 22 | fastapi | bug7.py | 31 | 0.8719 |
| 23 | fastapi | bug8.py | 67 | 0.8138 |
| 24 | fastapi | bug9.py | 6 | 0.9818 |
| 25 | fastapi | bug10.py | 95 | 0.6403 |
| 26 | fastapi | bug11.py | 30 | 0.8626 |
| 27 | fastapi | bug12.py | 228 | 0.4005 |
| 28 | fastapi | bug13.py | 10 | 0.9982 |
| 29 | keras | bug10.py | 1 | 1.0000 |
| 30 | keras | bug12.py | 1 | 0.9973 |
| 31 | keras | bug14.py | 2 | 0.9857 |
| 32 | keras | bug15.py | 1 | 0.9999 |
| 33 | keras | bug17.py | 3 | 0.9878 |
| 34 | keras | bug20.py | 1 | 1.0000 |
| 35 | keras | bug23.py | 37 | 0.6613 |
| 36 | keras | bug27.py | 1 | 0.9973 |
| 37 | keras | bug34.py | 1 | 0.9999 |
| 38 | keras | bug40.py | 1 | 0.9998 |
| 39 | luigi | bug1.py | — | — |
| 40 | luigi | bug2.py | — | — |
| 41 | luigi | bug3.py | — | — |
| 42 | luigi | bug4.py | — | — |
| 43 | luigi | bug5.py | — | — |
| 44 | luigi | bug6.py | — | — |
| 45 | luigi | bug7.py | — | — |
| 46 | luigi | bug8.py | — | — |
| 47 | luigi | bug9.py | — | — |
| 48 | mlib | bug10.py | 4 | 0.9899 |
| 49 | mlib | bug11.py | 397 | 0.9406 |
| 50 | mlib | bug12.py | 1 | 1.0000 |
| 51 | mlib | bug14.py | 1 | 0.9980 |
| 52 | mlib | bug17.py | 1 | 0.9973 |
| 53 | mlib | bug20.py | 70 | 0.9116 |
| 54 | mlib | bug23.py | 16 | 0.9843 |
| 55 | mlib | bug25.py | 63 | 0.9498 |
| 56 | mlib | bug27.py | 11 | 0.9736 |
| 57 | mlib | bug30.py | 33 | 0.9501 |
| 58 | pandas | bug100.py | 33 | 0.9930 |
| 59 | pandas | bug102.py | 9 | 0.9892 |
| 60 | pandas | bug105.py | 1 | 1.0000 |
| 61 | pandas | bug106.py | 9 | 0.9412 |
| 62 | pandas | bug107.py | 21 | 0.9997 |
| 63 | pandas | bug108.py | 1 | 0.9979 |
| 64 | pandas | bug110.py | 12 | 0.9753 |
| 65 | pandas | bug111.py | 21 | 0.9971 |
| 66 | pandas | bug112.py | 1 | 0.9982 |
| 67 | pandas | bug115.py | 5 | 0.9840 |
| 68 | pandas | bug117.py | 7 | 0.9601 |
| 69 | pandas | bug118.py | 6 | 0.9952 |
| 70 | pandas | bug120.py | 52 | 0.9932 |
| 71 | pandas | bug121.py | 13 | 0.9866 |
| 72 | pandas | bug125.py | 1 | 0.9973 |
| 73 | scrapy | bug1.py | — | — |
| 74 | scrapy | bug2.py | — | — |
| 75 | scrapy | bug3.py | — | — |
| 76 | scrapy | bug4.py | — | — |
| 77 | scrapy | bug5.py | — | — |
| 78 | scrapy | bug6.py | — | — |
| 79 | scrapy | bug7.py | — | — |
| 80 | scrapy | bug8.py | — | — |
| 81 | scrapy | bug9.py | — | — |
| 82 | spacy | bug1.py | 77 | 0.7633 |
| 83 | spacy | bug2.py | 1 | 0.9972 |
| 84 | spacy | bug3.py | 10 | 0.9865 |
| 85 | spacy | bug4.py | 60 | 0.9414 |
| 86 | spacy | bug5.py | 15 | 0.9718 |
| 87 | spacy | bug6.py | 5 | 0.9807 |
| 88 | spacy | bug7.py | 12 | 0.9942 |
| 89 | spacy | bug8.py | 1 | 0.9972 |
| 90 | spacy | bug9.py | 1 | 0.9972 |
| 91 | spacy | bug10.py | 4 | 0.9812 |
| 92 | tornado | bug1.py | — | — |
| 93 | tornado | bug2.py | — | — |
| 94 | tornado | bug3.py | — | — |
| 95 | tornado | bug4.py | — | — |
| 96 | tornado | bug5.py | — | — |
| 97 | tornado | bug6.py | — | — |
| 98 | tornado | bug7.py | — | — |
| 99 | tornado | bug8.py | — | — |
| 100 | tornado | bug9.py | — | — |

---

# Table 2: COT_TOT_C and COT_TOT_PYTHON — 10 libraries, 100 programs

| # | Library | Program | COT_TOT_C Lev | COT_TOT_C Cos | COT_TOT_PYTHON Lev | COT_TOT_PYTHON Cos |
|---|---------|---------|----------------|----------------|---------------------|---------------------|
| 1 | ansible | bug1 | 0 | 1.0000 | 1 | 0.9973 |
| 2 | ansible | bug2 | 5 | 0.9976 | 154 | 0.9532 |
| 3 | ansible | bug3 | 10 | 0.9895 | 1 | 0.9980 |
| 4 | ansible | bug4 | 19 | 0.9768 | 12 | 0.9810 |
| 5 | ansible | bug5 | 27 | 0.9838 | 8 | 0.9968 |
| 6 | ansible | bug6 | 18 | 0.9921 | 1 | 1.0000 |
| 7 | ansible | bug7 | 0 | 1.0000 | 1 | 0.9987 |
| 8 | ansible | bug8 | 0 | 1.0000 | 4 | 0.9996 |
| 9 | ansible | bug9 | 5 | 0.9969 | 5 | 0.9990 |
| 10 | black | bug1 | 8 | 0.9920 | 10 | 0.9942 |
| 11 | black | bug2 | 47 | 0.9881 | 121 | 0.9566 |
| 12 | black | bug3 | 80 | 0.9141 | 12 | 0.9704 |
| 13 | black | bug4 | 39 | 0.9543 | 1 | 0.9977 |
| 14 | black | bug5 | 0 | 1.0000 | 49 | 0.7152 |
| 15 | black | bug6 | 0 | 1.0000 | 77 | 0.9892 |
| 16 | black | bug7 | 5 | 0.9789 | 1 | 0.9989 |
| 17 | black | bug8 | 67 | 0.9562 | 17 | 0.9978 |
| 18 | black | bug9 | 0 | 1.0000 | 69 | 0.8365 |
| 19 | fastapi | bug1 | 1 | 0.9999 | 89 | 0.9867 |
| 20 | fastapi | bug2 | 5 | 0.9845 | 4 | 0.9897 |
| 21 | fastapi | bug5 | 20 | 0.9727 | 8 | 0.9751 |
| 22 | fastapi | bug7 | 14 | 0.9729 | 37 | 0.8091 |
| 23 | fastapi | bug8 | 5 | 0.9797 | 4 | 0.9877 |
| 24 | fastapi | bug9 | 7 | 0.9726 | 6 | 0.9818 |
| 25 | fastapi | bug10 | 1 | 0.9966 | 54 | 0.8304 |
| 26 | fastapi | bug11 | 1 | 0.9980 | 24 | 0.8381 |
| 27 | fastapi | bug12 | 20 | 0.9796 | 45 | 0.8846 |
| 28 | fastapi | bug13 | 29 | 0.8834 | 61 | 0.9981 |
| 29 | keras | bug10 | 8 | 0.9997 | 153 | 0.9944 |
| 30 | keras | bug12 | 1 | 0.9966 | 1 | 0.9973 |
| 31 | keras | bug14 | 6 | 0.9695 | 33 | 0.8567 |
| 32 | keras | bug15 | 66 | 0.9762 | 48 | 0.9935 |
| 33 | keras | bug17 | 30 | 0.9082 | 1 | 0.9976 |
| 34 | keras | bug20 | 65 | 0.9478 | 721 | 0.8276 |
| 35 | keras | bug23 | 19 | 0.9494 | 91 | 0.9932 |
| 36 | keras | bug27 | 1 | 0.9966 | 15 | 0.9616 |
| 37 | keras | bug34 | 41 | 0.9570 | 15 | 0.9987 |
| 38 | keras | bug40 | 11 | 0.9865 | 55 | 0.9760 |
| 39 | luigi | bug1 | 0 | 1.0000 | 6 | 0.9940 |
| 40 | luigi | bug2 | 85 | 0.9617 | 77 | 0.7702 |
| 41 | luigi | bug3 | 11 | 0.9902 | 27 | 0.9802 |
| 42 | luigi | bug4 | 6 | 0.9901 | 1 | 0.9977 |
| 43 | luigi | bug5 | 0 | 1.0000 | 55 | 0.9981 |
| 44 | luigi | bug6 | 0 | 1.0000 | 81 | 0.9969 |
| 45 | luigi | bug7 | 0 | 1.0000 | 1 | 0.9994 |
| 46 | luigi | bug8 | 33 | 0.9751 | 37 | 0.6076 |
| 47 | luigi | bug9 | 0 | 1.0000 | 136 | 0.9474 |
| 48 | mlib | bug10 | 5 | 0.9766 | 15 | 0.9827 |
| 49 | mlib | bug11 | 249 | 0.9524 | 1 | 1.0000 |
| 50 | mlib | bug12 | 8 | 0.9978 | 1 | 1.0000 |
| 51 | mlib | bug14 | 1 | 0.9977 | 1 | 0.9980 |
| 52 | mlib | bug17 | 1 | 0.9966 | 36 | 0.9527 |
| 53 | mlib | bug20 | 1 | 0.9993 | 107 | 0.9976 |
| 54 | mlib | bug23 | 6 | 0.9911 | 8 | 0.9920 |
| 55 | mlib | bug25 | 1 | 0.9994 | 9 | 0.9620 |
| 56 | mlib | bug27 | 11 | 0.9624 | 9 | 0.9751 |
| 57 | mlib | bug30 | 7 | 0.9872 | 1 | 0.9999 |
| 58 | pandas | bug100 | 70 | 0.9558 | 37 | 0.8987 |
| 59 | pandas | bug102 | 6 | 0.9803 | 1 | 0.9994 |
| 60 | pandas | bug105 | 22 | 0.9930 | 145 | 0.9977 |
| 61 | pandas | bug106 | 5 | 0.9817 | 1 | 0.9977 |
| 62 | pandas | bug107 | 6 | 0.9964 | 1 | 1.0000 |
| 63 | pandas | bug108 | 95 | 0.9676 | 5 | 0.9784 |
| 64 | pandas | bug110 | 36 | 0.9506 | 12 | 0.9753 |
| 65 | pandas | bug111 | 22 | 0.9538 | 21 | 0.9903 |
| 66 | pandas | bug112 | 100 | 0.8378 | 5 | 0.9812 |
| 67 | pandas | bug115 | 6 | 0.9818 | 4 | 0.9903 |
| 68 | pandas | bug117 | 13 | 0.9079 | 67 | 0.8251 |
| 69 | pandas | bug118 | 7 | 0.9772 | 6 | 0.9952 |
| 70 | pandas | bug120 | 22 | 0.9378 | 5 | 0.9996 |
| 71 | pandas | bug121 | 7 | 0.9832 | 21 | 0.9029 |
| 72 | pandas | bug125 | 5 | 0.9631 | 4 | 0.9818 |
| 73 | scrapy | bug1 | 0 | 1.0000 | 7 | 0.9938 |
| 74 | scrapy | bug2 | 14 | 0.9822 | 6 | 0.9943 |
| 75 | scrapy | bug3 | 0 | 1.0000 | 1 | 0.9988 |
| 76 | scrapy | bug4 | 15 | 0.9914 | 8 | 0.9865 |
| 77 | scrapy | bug5 | 0 | 1.0000 | 1 | 0.9973 |
| 78 | scrapy | bug6 | 0 | 1.0000 | 793 | 0.4168 |
| 79 | scrapy | bug7 | 17 | 0.9866 | 6 | 0.9815 |
| 80 | scrapy | bug8 | 2 | 0.9646 | 1 | 0.9973 |
| 81 | scrapy | bug9 | 0 | 1.0000 | 4 | 0.9814 |
| 82 | spacy | bug1 | 14 | 0.9827 | 93 | 0.6742 |
| 83 | spacy | bug2 | 29 | 0.9186 | 1 | 0.9972 |
| 84 | spacy | bug3 | 11 | 0.9835 | 10 | 0.9865 |
| 85 | spacy | bug4 | 1 | 0.9992 | 1 | 0.9991 |
| 86 | spacy | bug5 | 4 | 0.9796 | 4 | 0.9921 |
| 87 | spacy | bug6 | 26 | 0.9606 | 108 | 0.7413 |
| 88 | spacy | bug7 | 12 | 0.9860 | 94 | 0.8018 |
| 89 | spacy | bug8 | 8 | 0.9694 | 1 | 0.9972 |
| 90 | spacy | bug9 | 12 | 0.9860 | 1 | 0.9972 |
| 91 | spacy | bug10 | 1 | 0.9966 | 1 | 0.9973 |
| 92 | tornado | bug1 | 0 | 1.0000 | 1 | 0.9991 |
| 93 | tornado | bug2 | 9 | 0.9838 | 26 | 0.7140 |
| 94 | tornado | bug3 | 0 | 1.0000 | 39 | 0.9781 |
| 95 | tornado | bug4 | 28 | 0.8946 | 19 | 0.9976 |
| 96 | tornado | bug5 | 0 | 1.0000 | 16 | 0.9774 |
| 97 | tornado | bug6 | 0 | 1.0000 | 9 | 0.9803 |
| 98 | tornado | bug7 | 7 | 0.9823 | 11 | 0.9829 |
| 99 | tornado | bug8 | 22 | 0.8792 | 1 | 0.9973 |
| 100 | tornado | bug9 | 11 | 0.7646 | 4 | 0.9815 |

---

# Table 3: C — graph_based_LD, english_cot_tot, graph_based_cos_sim, english_tot_cot

(graph_based = TOT, english = COT from COT_TOT_C.)

| # | Library | Program | graph_based_LD | english_cot_tot | graph_based_cos_sim | english_tot_cot |
|---|---------|---------|-----------------|-----------------|---------------------|-----------------|
| 1 | ansible | bug1 | 0 | 0 | 1.0000 | 1.0000 |
| 2 | ansible | bug2 | 5 | 0 | 0.9976 | 1.0000 |
| 3 | ansible | bug3 | 10 | 0 | 0.9895 | 1.0000 |
| 4 | ansible | bug4 | 19 | 0 | 0.9768 | 1.0000 |
| 5 | ansible | bug5 | 27 | 10 | 0.9838 | 0.9778 |
| 6 | ansible | bug6 | 18 | 0 | 0.9921 | 1.0000 |
| 7 | ansible | bug7 | 0 | 4 | 1.0000 | 0.9929 |
| 8 | ansible | bug8 | 0 | 22 | 1.0000 | 0.9366 |
| 9 | ansible | bug9 | 5 | 0 | 0.9969 | 1.0000 |
| 10 | black | bug1 | 8 | 0 | 0.9920 | 1.0000 |
| 11 | black | bug2 | 47 | 0 | 0.9881 | 1.0000 |
| 12 | black | bug3 | 80 | 0 | 0.9141 | 1.0000 |
| 13 | black | bug4 | 39 | 26 | 0.9543 | 0.9530 |
| 14 | black | bug5 | 0 | 20 | 1.0000 | 0.9909 |
| 15 | black | bug6 | 0 | 31 | 1.0000 | 0.9931 |
| 16 | black | bug7 | 5 | 0 | 0.9789 | 1.0000 |
| 17 | black | bug8 | 67 | 0 | 0.9562 | 1.0000 |
| 18 | black | bug9 | 0 | 0 | 1.0000 | 1.0000 |
| 19 | fastapi | bug1 | 1 | 261 | 0.9999 | 0.9813 |
| 20 | fastapi | bug2 | 5 | 1 | 0.9845 | 0.9984 |
| 21 | fastapi | bug5 | 20 | 1 | 0.9727 | 0.9982 |
| 22 | fastapi | bug7 | 14 | 8 | 0.9729 | 0.9776 |
| 23 | fastapi | bug8 | 5 | 1 | 0.9797 | 0.9979 |
| 24 | fastapi | bug9 | 7 | 22 | 0.9726 | 0.9690 |
| 25 | fastapi | bug10 | 1 | 1 | 0.9966 | 0.9966 |
| 26 | fastapi | bug11 | 1 | 1 | 0.9980 | 0.9980 |
| 27 | fastapi | bug12 | 20 | 1 | 0.9796 | 0.9988 |
| 28 | fastapi | bug13 | 29 | 16 | 0.8834 | 0.9897 |
| 29 | keras | bug10 | 8 | 1 | 0.9997 | 1.0000 |
| 30 | keras | bug12 | 1 | 1 | 0.9966 | 0.9966 |
| 31 | keras | bug14 | 6 | 1 | 0.9695 | 0.9980 |
| 32 | keras | bug15 | 66 | 1 | 0.9762 | 0.9993 |
| 33 | keras | bug17 | 30 | 1 | 0.9082 | 0.9977 |
| 34 | keras | bug20 | 65 | 1 | 0.9478 | 0.9996 |
| 35 | keras | bug23 | 19 | 1 | 0.9494 | 0.9985 |
| 36 | keras | bug27 | 1 | 1 | 0.9966 | 0.9966 |
| 37 | keras | bug34 | 41 | 1 | 0.9570 | 0.9994 |
| 38 | keras | bug40 | 11 | 1 | 0.9865 | 0.9991 |
| 39 | luigi | bug1 | 0 | 0 | 1.0000 | 1.0000 |
| 40 | luigi | bug2 | 85 | 2 | 0.9617 | 0.9979 |
| 41 | luigi | bug3 | 11 | 30 | 0.9902 | 0.9816 |
| 42 | luigi | bug4 | 6 | 13 | 0.9901 | 0.9814 |
| 43 | luigi | bug5 | 0 | 38 | 1.0000 | 0.9835 |
| 44 | luigi | bug6 | 0 | 23 | 1.0000 | 0.9773 |
| 45 | luigi | bug7 | 0 | 8 | 1.0000 | 0.9967 |
| 46 | luigi | bug8 | 33 | 0 | 0.9751 | 1.0000 |
| 47 | luigi | bug9 | 0 | 2 | 1.0000 | 0.9993 |
| 48 | mlib | bug10 | 5 | 1 | 0.9766 | 0.9978 |
| 49 | mlib | bug11 | 249 | 6 | 0.9524 | 0.9987 |
| 50 | mlib | bug12 | 8 | 1 | 0.9978 | 0.9998 |
| 51 | mlib | bug14 | 1 | 1 | 0.9977 | 0.9977 |
| 52 | mlib | bug17 | 1 | 1 | 0.9966 | 0.9966 |
| 53 | mlib | bug20 | 1 | 1 | 0.9993 | 0.9993 |
| 54 | mlib | bug23 | 6 | 6 | 0.9911 | 0.9841 |
| 55 | mlib | bug25 | 1 | 1 | 0.9994 | 0.9994 |
| 56 | mlib | bug27 | 11 | 1 | 0.9624 | 0.9975 |
| 57 | mlib | bug30 | 7 | 1 | 0.9872 | 0.9992 |
| 58 | pandas | bug100 | 70 | 53 | 0.9558 | 0.9851 |
| 59 | pandas | bug102 | 6 | 16 | 0.9803 | 0.9745 |
| 60 | pandas | bug105 | 22 | 1 | 0.9930 | 0.9998 |
| 61 | pandas | bug106 | 5 | 1 | 0.9817 | 0.9986 |
| 62 | pandas | bug107 | 6 | 1 | 0.9964 | 0.9997 |
| 63 | pandas | bug108 | 95 | 1 | 0.9676 | 0.9982 |
| 64 | pandas | bug110 | 36 | 1 | 0.9506 | 0.9978 |
| 65 | pandas | bug111 | 22 | 1 | 0.9538 | 0.9994 |
| 66 | pandas | bug112 | 100 | 1 | 0.8378 | 0.9980 |
| 67 | pandas | bug115 | 6 | 5 | 0.9818 | 0.9741 |
| 68 | pandas | bug117 | 13 | 13 | 0.9079 | 0.9079 |
| 69 | pandas | bug118 | 7 | 1 | 0.9772 | 0.9985 |
| 70 | pandas | bug120 | 22 | 1 | 0.9378 | 0.9991 |
| 71 | pandas | bug121 | 7 | 1 | 0.9832 | 0.9985 |
| 72 | pandas | bug125 | 5 | 37 | 0.9631 | 0.9291 |
| 73 | scrapy | bug1 | 0 | 20 | 1.0000 | 0.9968 |
| 74 | scrapy | bug2 | 14 | 0 | 0.9822 | 1.0000 |
| 75 | scrapy | bug3 | 0 | 0 | 1.0000 | 1.0000 |
| 76 | scrapy | bug4 | 15 | 15 | 0.9914 | 0.9912 |
| 77 | scrapy | bug5 | 0 | 0 | 1.0000 | 1.0000 |
| 78 | scrapy | bug6 | 0 | 0 | 1.0000 | 1.0000 |
| 79 | scrapy | bug7 | 17 | 0 | 0.9866 | 1.0000 |
| 80 | scrapy | bug8 | 2 | 0 | 0.9646 | 1.0000 |
| 81 | scrapy | bug9 | 0 | 0 | 1.0000 | 1.0000 |
| 82 | spacy | bug1 | 14 | 8 | 0.9827 | 0.9859 |
| 83 | spacy | bug2 | 29 | 1 | 0.9186 | 0.9966 |
| 84 | spacy | bug3 | 11 | 11 | 0.9835 | 0.9835 |
| 85 | spacy | bug4 | 1 | 1 | 0.9992 | 0.9992 |
| 86 | spacy | bug5 | 4 | 1 | 0.9796 | 0.9976 |
| 87 | spacy | bug6 | 26 | 1 | 0.9606 | 0.9979 |
| 88 | spacy | bug7 | 12 | 12 | 0.9860 | 0.9860 |
| 89 | spacy | bug8 | 8 | 1 | 0.9694 | 0.9966 |
| 90 | spacy | bug9 | 12 | 12 | 0.9860 | 0.9860 |
| 91 | spacy | bug10 | 1 | 1 | 0.9966 | 0.9966 |
| 92 | tornado | bug1 | 0 | 7 | 1.0000 | 0.9924 |
| 93 | tornado | bug2 | 9 | 0 | 0.9838 | 1.0000 |
| 94 | tornado | bug3 | 0 | 0 | 1.0000 | 1.0000 |
| 95 | tornado | bug4 | 28 | 0 | 0.8946 | 1.0000 |
| 96 | tornado | bug5 | 0 | 0 | 1.0000 | 1.0000 |
| 97 | tornado | bug6 | 0 | 40 | 1.0000 | 0.9691 |
| 98 | tornado | bug7 | 7 | 0 | 0.9823 | 1.0000 |
| 99 | tornado | bug8 | 22 | 0 | 0.8792 | 1.0000 |
| 100 | tornado | bug9 | 11 | 0 | 0.7646 | 1.0000 |

---

# Table 4: Python — graph_based_LD, english_cot_tot, graph_based_cos_sim, english_tot_cot

(graph_based = baseline from results/; english_cot_tot = COT, english_tot_cot = TOT from COT_TOT_PYTHON.)

| # | Library | Program | graph_based_LD | english_cot_tot | graph_based_cos_sim | english_tot_cot |
|---|---------|---------|-----------------|-----------------|---------------------|-----------------|
| 1 | ansible | bug1.py | — | 1 | — | 0.9973 |
| 2 | ansible | bug2.py | — | 1 | — | 0.9532 |
| 3 | ansible | bug3.py | — | 1 | — | 0.9980 |
| 4 | ansible | bug4.py | — | 1 | — | 0.9810 |
| 5 | ansible | bug5.py | — | 1 | — | 0.9968 |
| 6 | ansible | bug6.py | — | 1 | — | 1.0000 |
| 7 | ansible | bug7.py | — | 1 | — | 0.9987 |
| 8 | ansible | bug8.py | — | 1 | — | 0.9996 |
| 9 | ansible | bug9.py | — | 90 | — | 0.9990 |
| 10 | black | bug1.py | — | 1 | — | 0.9942 |
| 11 | black | bug2.py | — | 1 | — | 0.9566 |
| 12 | black | bug3.py | — | 1 | — | 0.9704 |
| 13 | black | bug4.py | — | 1 | — | 0.9977 |
| 14 | black | bug5.py | — | 1 | — | 0.7152 |
| 15 | black | bug6.py | — | 100 | — | 0.9892 |
| 16 | black | bug7.py | — | 1 | — | 0.9989 |
| 17 | black | bug8.py | — | 32 | — | 0.9978 |
| 18 | black | bug9.py | — | 5 | — | 0.8365 |
| 19 | fastapi | bug1.py | 60 | 1 | 0.9994 | 0.9867 |
| 20 | fastapi | bug2.py | 8 | 1 | 0.9594 | 0.9897 |
| 21 | fastapi | bug5.py | 3 | 1 | 0.9934 | 0.9751 |
| 22 | fastapi | bug7.py | 31 | 1 | 0.8719 | 0.8091 |
| 23 | fastapi | bug8.py | 67 | 1 | 0.8138 | 0.9877 |
| 24 | fastapi | bug9.py | 6 | 1 | 0.9818 | 0.9818 |
| 25 | fastapi | bug10.py | 95 | 1 | 0.6403 | 0.8304 |
| 26 | fastapi | bug11.py | 30 | 24 | 0.8626 | 0.8381 |
| 27 | fastapi | bug12.py | 228 | 1 | 0.4005 | 0.8846 |
| 28 | fastapi | bug13.py | 10 | 65 | 0.9982 | 0.9981 |
| 29 | keras | bug10.py | 1 | 1 | 1.0000 | 0.9944 |
| 30 | keras | bug12.py | 1 | 1 | 0.9973 | 0.9973 |
| 31 | keras | bug14.py | 2 | 16 | 0.9857 | 0.8567 |
| 32 | keras | bug15.py | 1 | 1 | 0.9999 | 0.9935 |
| 33 | keras | bug17.py | 3 | 1 | 0.9878 | 0.9976 |
| 34 | keras | bug20.py | 1 | 324 | 1.0000 | 0.8276 |
| 35 | keras | bug23.py | 37 | 20 | 0.6613 | 0.9932 |
| 36 | keras | bug27.py | 1 | 1 | 0.9973 | 0.9616 |
| 37 | keras | bug34.py | 1 | 1 | 0.9999 | 0.9987 |
| 38 | keras | bug40.py | 1 | 1 | 0.9998 | 0.9760 |
| 39 | luigi | bug1.py | — | 6 | — | 0.9940 |
| 40 | luigi | bug2.py | — | 1 | — | 0.7702 |
| 41 | luigi | bug3.py | — | 1 | — | 0.9802 |
| 42 | luigi | bug4.py | — | 1 | — | 0.9977 |
| 43 | luigi | bug5.py | — | 1 | — | 0.9981 |
| 44 | luigi | bug6.py | — | 7 | — | 0.9969 |
| 45 | luigi | bug7.py | — | 1 | — | 0.9994 |
| 46 | luigi | bug8.py | — | 1 | — | 0.6076 |
| 47 | luigi | bug9.py | — | 25 | — | 0.9474 |
| 48 | mlib | bug10.py | 4 | 1 | 0.9899 | 0.9827 |
| 49 | mlib | bug11.py | 397 | 51 | 0.9406 | 1.0000 |
| 50 | mlib | bug12.py | 1 | 89 | 1.0000 | 1.0000 |
| 51 | mlib | bug14.py | 1 | 1 | 0.9980 | 0.9980 |
| 52 | mlib | bug17.py | 1 | 1 | 0.9973 | 0.9527 |
| 53 | mlib | bug20.py | 70 | 79 | 0.9116 | 0.9976 |
| 54 | mlib | bug23.py | 16 | 9 | 0.9843 | 0.9920 |
| 55 | mlib | bug25.py | 63 | 15 | 0.9498 | 0.9620 |
| 56 | mlib | bug27.py | 11 | 1 | 0.9736 | 0.9751 |
| 57 | mlib | bug30.py | 33 | 1 | 0.9501 | 0.9999 |
| 58 | pandas | bug100.py | 33 | 32 | 0.9930 | 0.8987 |
| 59 | pandas | bug102.py | 9 | 1 | 0.9892 | 0.9994 |
| 60 | pandas | bug105.py | 1 | 1 | 1.0000 | 0.9977 |
| 61 | pandas | bug106.py | 9 | 1 | 0.9412 | 0.9977 |
| 62 | pandas | bug107.py | 21 | 1 | 0.9997 | 1.0000 |
| 63 | pandas | bug108.py | 1 | 5 | 0.9979 | 0.9784 |
| 64 | pandas | bug110.py | 12 | 1 | 0.9753 | 0.9753 |
| 65 | pandas | bug111.py | 21 | 6 | 0.9971 | 0.9903 |
| 66 | pandas | bug112.py | 1 | 92 | 0.9982 | 0.9812 |
| 67 | pandas | bug115.py | 5 | 1 | 0.9840 | 0.9903 |
| 68 | pandas | bug117.py | 7 | 34 | 0.9601 | 0.8251 |
| 69 | pandas | bug118.py | 6 | 6 | 0.9952 | 0.9952 |
| 70 | pandas | bug120.py | 52 | 1 | 0.9932 | 0.9996 |
| 71 | pandas | bug121.py | 13 | 1 | 0.9866 | 0.9029 |
| 72 | pandas | bug125.py | 1 | 1 | 0.9973 | 0.9818 |
| 73 | scrapy | bug1.py | — | 1 | — | 0.9938 |
| 74 | scrapy | bug2.py | — | 1 | — | 0.9943 |
| 75 | scrapy | bug3.py | — | 1 | — | 0.9988 |
| 76 | scrapy | bug4.py | — | 1 | — | 0.9865 |
| 77 | scrapy | bug5.py | — | 1 | — | 0.9973 |
| 78 | scrapy | bug6.py | — | 1 | — | 0.4168 |
| 79 | scrapy | bug7.py | — | 45 | — | 0.9815 |
| 80 | scrapy | bug8.py | — | 1 | — | 0.9973 |
| 81 | scrapy | bug9.py | — | 1 | — | 0.9814 |
| 82 | spacy | bug1.py | 77 | 1074 | 0.7633 | 0.6742 |
| 83 | spacy | bug2.py | 1 | 1 | 0.9972 | 0.9972 |
| 84 | spacy | bug3.py | 10 | 10 | 0.9865 | 0.9865 |
| 85 | spacy | bug4.py | 60 | 17 | 0.9414 | 0.9991 |
| 86 | spacy | bug5.py | 15 | 1 | 0.9718 | 0.9921 |
| 87 | spacy | bug6.py | 5 | 5 | 0.9807 | 0.7413 |
| 88 | spacy | bug7.py | 12 | 26 | 0.9942 | 0.8018 |
| 89 | spacy | bug8.py | 1 | 1 | 0.9972 | 0.9972 |
| 90 | spacy | bug9.py | 1 | 1 | 0.9972 | 0.9972 |
| 91 | spacy | bug10.py | 4 | 1 | 0.9812 | 0.9973 |
| 92 | tornado | bug1.py | — | 14 | — | 0.9991 |
| 93 | tornado | bug2.py | — | 1 | — | 0.7140 |
| 94 | tornado | bug3.py | — | 17 | — | 0.9781 |
| 95 | tornado | bug4.py | — | 5 | — | 0.9976 |
| 96 | tornado | bug5.py | — | 1 | — | 0.9774 |
| 97 | tornado | bug6.py | — | 9 | — | 0.9803 |
| 98 | tornado | bug7.py | — | 13 | — | 0.9829 |
| 99 | tornado | bug8.py | — | 1 | — | 0.9973 |
| 100 | tornado | bug9.py | — | 1 | — | 0.9815 |