import difflib

def diff_files(generated_file, corr_file):
      file_text = []
      for file_name in [generated_file, corr_file]:
        with open(file_name) as f:
          file_text.append(f.readlines())
      diff = ""
      for line in difflib.unified_diff(file_text[0], file_text[1]):
          diff += str(line)
      return diff
