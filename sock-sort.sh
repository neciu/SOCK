# The MIT License (MIT)
#
# Copyright (c) 2013 
#     Tomasz Netczuk (netczuk.tomasz at gmail.com)
#     Dariusz Seweryn (dariusz.seweryn at gmail.com)
#     https://github.com/neciu/SOCK
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


echo "pre-commit pysock script start"

temp_file_name="sock_temp_file_which_will_be_deleted_automatically"
script_name="pysock/sock.py"

######## Getting staged files paths and dumping to file
git diff --name-only --cached >> $temp_file_name

######## Looking for path of project.pbxproj file
file="$temp_file_name"
while read line 
do
	if [[ $line =~ .*project.pbxproj.* ]]; then
		pathToProjectPbxproj=$line
		break
	fi
done <"$file"

######## Running python script which sorts the project.pbxproj sections if path found (need to change the python script file here)
[ -n "$pathToProjectPbxproj" ] && python $script_name $pathToProjectPbxproj

##### Test changes
###chmod 777 $pathToProjectPbxproj
###echo someChangeInsertedInFile >> $pathToProjectPbxproj

######## Re-adding sorted project.pbxproj if path exists
[ -n "$pathToProjectPbxproj" ] && git add $pathToProjectPbxproj

######## Cleaning up the file
rm $temp_file_name

echo "pre-commit pysock script end"