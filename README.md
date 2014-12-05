RecoverMe
===========

Uses TSK tools to pull files from a computer.  This was made for two purposes.  First, this is made for the people that accidently delete files that they didn't mean to.  It will try to recover them if the option is set.  Secondly, this is used for failing drives.  If you are having issues reading from a drive (ie.  System no longer recognizes the partition and asks you to format the drive each time you plug it in) and want to save your data give this ago.  

I originally added threading but do to trying to use it on bad drives I decided that simultaneous read/writes were probably not the best.  So it is slow, but it is the best thing out there for the job.  

Requirements
============
You will need TSK, you can get that here http://sourceforge.net/projects/sleuthkit/files/sleuthkit/4.1.3/sleuthkit-4.1.3-win32.zip/download .  I built this for Windows, but after reviewing the code, I believe it is cross platform.
