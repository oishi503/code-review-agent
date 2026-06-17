def parse_diff(diff_text):
    files = []
    current_file = None
    current_hunks = []
    current_hunk_lines = []
    current_line_number = 0

    for line in diff_text.split('\n'):
        if line.startswith('diff --git'):
            if current_file:
                if current_hunk_lines:
                    current_hunks.append({
                        'lines': current_hunk_lines,
                        'start_line': current_line_number
                    })
                files.append({
                    'filename': current_file,
                    'hunks': current_hunks
                })
            current_file = line.split(' b/')[-1]
            current_hunks = []
            current_hunk_lines = []

        elif line.startswith('@@'):
            if current_hunk_lines:
                current_hunks.append({
                    'lines': current_hunk_lines,
                    'start_line': current_line_number
                })
            current_hunk_lines = []
            try:
                current_line_number = int(line.split('+')[1].split(',')[0])
            except:
                current_line_number = 0

        elif line.startswith('+') and not line.startswith('+++'):
            current_hunk_lines.append({
                'content': line[1:],
                'line_number': current_line_number,
                'type': 'added'
            })
            current_line_number += 1

        elif line.startswith('-') and not line.startswith('---'):
            current_hunk_lines.append({
                'content': line[1:],
                'line_number': current_line_number,
                'type': 'removed'
            })

        else:
            current_line_number += 1

    if current_file:
        if current_hunk_lines:
            current_hunks.append({
                'lines': current_hunk_lines,
                'start_line': current_line_number
            })
        files.append({
            'filename': current_file,
            'hunks': current_hunks
        })

    return files