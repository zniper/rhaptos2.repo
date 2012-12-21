
#These might be parameters but this assumes ghpages.sh is in package top level

ABSDIR=$( cd $(dirname $0) ; pwd -P )
SRCDOCS=$ABSDIR/docs/_build/html
TMPREPO=/tmp/docs/repo

### get the last commit message
cd $SRCDOCS
MSG="Adding gh-pages docs for `git log -1 --pretty=short --abbrev-commit`"


### clear the decks
rm -rf $TMPREPO
mkdir -p -m 0755 $TMPREPO

### checkout gh-pages into TMP
git clone git@github.com:Connexions/rhaptos2.repo.git $TMPREPO
cd $TMPREPO
git checkout gh-pages

### cp the docs over and commit
cp -r $SRCDOCS/ $TMPREPO

git add -A
git commit -m "$MSG" && git push origin gh-pages
