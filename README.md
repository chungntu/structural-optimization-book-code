# Structural Optimization Book Code

This repository contains the source code examples used in the book **Tối ưu kết cấu – Lý thuyết và ứng dụng trong công trình cầu** (*Structural Optimization – Theory and Applications in Bridge Engineering*), by Bùi Tiến Thành and Trương Thành Chung, University of Transport and Communications (Hanoi).

## Structure


- `examples/`: full code package used for the book, grouped by chapter/example number. This includes scripts, generated figures, structural model files, and truss model support files.

## Chapter 9 – bridge applications

- `Code 9.1`: composite steel I-girder optimization according to TCVN 11823:2017 (SQP, differential evolution, Lagrange multipliers, discrete design, epsilon-constraint trade-off curve).
- `Code 9.2`: tuned mass damper optimization for a high-speed railway bridge under the HSLM-A trains of EN 1991-2 (Den Hartog, contour map, epigraph SQP, GA, Pareto front).
- `Code 9.3`: finite element model updating of the Nam O railway steel truss bridge from measured frequencies (sensitivity analysis, bounded least squares, GA).

Run the scripts in each folder in the order model → optimization → analysis → figures; the `*_results.json` files hold the results used in the book.

## Languages

- MATLAB / GNU Octave
- Python (`numpy`, `scipy`, `matplotlib`)

## Notes

The code is organized to match the numbering used in the book. Some scripts may require MATLAB, GNU Octave, Python, or common scientific packages depending on the example.

## Tiếng Việt

Kho mã nguồn này gồm các ví dụ code được dùng trong sách **Tối ưu kết cấu – Lý thuyết và ứng dụng trong công trình cầu** (GS.TS. Bùi Tiến Thành, ThS. Trương Thành Chung – Trường Đại học Giao thông Vận tải).


- `examples/`: bộ code đầy đủ dùng cho sách, theo đúng số thứ tự trong sách; bao gồm script, hình kết quả, file mô hình kết cấu và các file hỗ trợ mô hình giàn.
- Chương 9 (ứng dụng trong công trình cầu): Code 9.1 – tối ưu dầm thép chữ I liên hợp theo TCVN 11823:2017; Code 9.2 – tối ưu bộ giảm chấn khối lượng cho cầu đường sắt cao tốc dưới các đoàn tàu HSLM-A; Code 9.3 – hiệu chỉnh mô hình cầu giàn thép đường sắt Nam Ô từ dữ liệu đo.

The book PDF and other generated or reference PDFs are kept in the parent project's local archives and are not distributed from this code repository.
