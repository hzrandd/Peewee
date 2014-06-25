import errno
import optparse
import os
import sys
import time

BASE = '/var/lock/sm'


def _get_age_days(secs):
    return float(time.time() - secs) / 86400


def _parse_args():
    parser = optparse.OptionParser()
    parser.add_option("-d", "--dry-run",
                      action="store_true", dest="dry_run", default=False,
                      help="don't actually remove locks")
    parser.add_option("-l", "--limit",
                      action="store", type='int', dest="limit",
                      default=sys.maxint,
                      help="max number of locks to delete (default: no limit)")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="don't print status messages to stdout")

    options, args = parser.parse_args()

    try:
        days_old = int(args[0])
    except (IndexError, ValueError):
        parser.print_help()
        sys.exit(1)

    return options, days_old


def main():
    options, days_old = _parse_args()

    if not os.path.exists(BASE):
        print >> sys.stderr, "error: '%s' doesn't exist. Make sure you're"\
                             " running this on the dom0." % BASE
        sys.exit(1)

    lockpaths_removed = 0
    nspaths_removed = 0

    for nsname in os.listdir(BASE)[:options.limit]:
        nspath = os.path.join(BASE, nsname)

        if not os.path.isdir(nspath):
            continue

        # Remove old lockfiles
        removed = 0
        locknames = os.listdir(nspath)
        for lockname in locknames:
            lockpath = os.path.join(nspath, lockname)
            lock_age_days = _get_age_days(os.path.getmtime(lockpath))
            if lock_age_days > days_old:
                lockpaths_removed += 1
                removed += 1

                if options.verbose:
                    print 'Removing old lock: %03d %s' % (lock_age_days,
                                                          lockpath)

                if not options.dry_run:
                    os.unlink(lockpath)

        # Remove empty namespace paths
        if len(locknames) == removed:
            nspaths_removed += 1

            if options.verbose:
                print 'Removing empty namespace: %s' % nspath

            if not options.dry_run:
                try:
                    os.rmdir(nspath)
                except OSError, e:
                    if e.errno == errno.ENOTEMPTY:
                        print >> sys.stderr, "warning: directory '%s'"\
                                             " not empty" % nspath
                    else:
                        raise

    if options.dry_run:
        print "** Dry Run **"

    print "Total locks removed: ", lockpaths_removed
    print "Total namespaces removed: ", nspaths_removed


if __name__ == '__main__':
    main()
