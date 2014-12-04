#############################################################################
##
##  Tool:      SaveMyDrive
##  Version:   1.0
##  Developer: Brandon Helms
##  Notes:     This requires TSK binaries (mmls, fls, icat).  I do not 
##             threading because some of the drives were in bad states 
##             already.  If on Windows, run as Administrator!!
##
#############################################################################
import os
import subprocess

from re import findall
from sys import exit

####################[ EDIT THE FOLLOWING DATA ]##############################
MMLS_TOOL = 'mmls.exe'          #location of mmls.exe
FLS_TOOL = 'fls.exe'            #location of fls.exe
ICAT_TOOL = 'icat.exe'          #location of icat.exe

DRIVE = r'\\.\PhysicalDrive0'   #PhyiscalDrive of analysis
OUTPUT_DIR = r'd:\test'         #Where to copy all the files to
DELETEDFILES_ONLY = False       #Set this flag if you only want to recover deleted files
#####################[ DONT EDIT BELOW HERE ]################################

def getOffset():
    print 'Checking for partitions on %s' %DRIVE
    try:
        result = subprocess.check_output('%s %s' %(MMLS_TOOL, DRIVE))
    except:
        print 'Ok, I can tell you are not running as Administrator, try it again.'
        sys.exit(1)
    parts = []
            
    #Going to assume they have only one partition
    for line in result.split('\r\n'):
        try:
            parts.append(int(line.split('   ')[1]))
        except:
            continue
            
    print 'I found %d different partitions that I will pull data from.' %len(parts) 
    return parts

def dirWalk():
    print '\nTrying to access %s' %partitionName
    cmdOptions = '-F -r'
    
    if DELETEDFILES_ONLY:
        cmdOptions += ' -d'
    try:
        result = subprocess.check_output('%s -o%d %s %s' %(FLS_TOOL, offset, cmdOptions, DRIVE))
    except subprocess.CalledProcessError:
        print '\tWell, I guess there isn\'t crap we care about on that one.'
        return False
        
    data = {}
    excludeChars = ':*'
    for line in result.split('\r\n'):
        dontPost = False
        if not line.startswith('r/r'):
            continue
        try:
            inode = findall('(\d.*?):', line)[0].split('(realloc)')[0]
            path = findall(':(.*)', line)[0].strip()
            for char in excludeChars:
                if char in path:
                    dontPost = True
                    continue
        except IndexError:
            continue 
        
        if not dontPost:
            data[inode] = path
    
    print '\tOk, I got\'s me some data. YAH'
    return data

def recreateDirStruct():
    print 'Copying files, this might take some time...'
    print '\tI am trying to put the data in "%s"' %os.path.normpath(os.path.join(OUTPUT_DIR, partitionName))
    
    for key in data:
        fullPath = os.path.normpath(os.path.join(OUTPUT_DIR, partitionName, data[key]))
        
        if not os.path.exists(os.path.split(fullPath)[0]):
            os.makedirs(os.path.split(fullPath)[0])
            
        try:
            os.system('%s -o%d %s %s > "%s"' %(ICAT_TOOL, offset, DRIVE, key, fullPath))
        except:
            print '\tDon\'t be alarmed but I could not get a good hold of "%s"' % fullPath
            continue
    
    print 'Grabbed everything I could from %s, moving on.' %partitionName

if __name__ == '__main__':
    offsets = getOffset()
    count = 1
    
    for offset in offsets:
        partitionName = 'partition%d' %count
        data = dirWalk()
        if data:
            recreateDirStruct()
        count += 1
    print 'And ...... we are done here.'
