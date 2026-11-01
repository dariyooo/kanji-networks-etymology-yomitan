# Vendored sources

Frozen third-party data the dictionary is built from, one folder per source (`vendored_sources/{name}/`).

Every folder contains a `README.md` with:

* Origin: URL (and commit / version) the data was copied from
* License of the data
* Date it was retrieved

## kanjinetworks

* Origin: [acoomans/kanjinetworks](https://github.com/acoomans/kanjinetworks) 0.1.8, ported to Python 3 here
  (otherwise unchanged), including the Kanji Networks PDF in `kanjinetworks/data/`
* License: code MIT (Arnaud Coomans), PDF by Lawrence J. Howell and Hikaru Morimoto, released when
  [kanjinetworks.com](http://www.kanjinetworks.com) closed in August 2016
* Retrieved: 2026-03-14
