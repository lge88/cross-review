Usage: cross_review.py [file] [N] [OPTIONS]
  Given a list of peers, randomly assign reviewers to each peer.

  file
    The file name of list of ids. Use '-' to read file from stdin.

  N
    Number of reviewers. Default is 2.

  -a or --all
    Print both --to-review and --reviewed-by. By default, -a is
    enabled.

  -t or --to-review
    For each reviewer, print the list of ids to be reviewed.

  -b or --reviewed-by
    For each reviewee, print the list of ids by whom he/she
    is reviewed.

  -h or --help
    Print this help message.
