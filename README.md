SOCK
====

**Simple Omitter of Conflicts Kit** - tool that prevents some of merge conflicts in .pbxproj file in **Xcode** projects

How does it work?
----
Right now we have only one way to deal with this problem: **sock-sort** script. It sorts critical sections in .pbxproj file such as:
- PBXBuildFile
- PBXFileReference
- PBXGroup
- PBXResourcesBuildPhase
- PBXSourcesBuildPhase

Sorted pbxproj file is less vulnerable to merge conflicts because in unsorted file all new resources, files and so on are added at the end of the section. In our approach new files are added in alphabetically sorted list so there is significant chance (which gets bigger with every file added to the project) to insert this file in different line - which is handled better by git merge tools.

Sorting script is ran every time you commit changes of .pbxproj file.

How to use it?
---
1. First off you need to clone **pysock** directory and **sock-sort.sh** script into root of your project.
2. Next you need to create git hook: `ln -s ../../sock-sort.sh .git/hooks/pre-commit`
3. Add permissions `chmod 555 .git/hooks/pre-commit` 
4. In your master branch sort .pbxproj file for the first time by changing something in .pbxproj and commiting **or** manually running sorting script: `python pysock/sock.py AwesomeProject.xcodeproj/project.pbxproj` and then commiting changes.
5. And your done! Every next branch will have sorted .pbxproj file and every time you merge you'll see less conflicts.

**Warning** it is required that every person in team uses this script otherwise it will generate more conflicts.

License
---
    The MIT License (MIT)

    Copyright (c) 2013
        Tomasz Netczuk (netczuk.tomasz at gmail.com), 
        Dariusz Seweryn (dariusz.seweryn at gmail.com), 
        https://github.com/neciu/SOCK

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

Team
---
Tomasz Netczuk [@neciu](https://github.com/neciu)  

Dariusz Seweryn [@dariuszseweryn](https://github.com/dariuszseweryn)  

---

Thanks [@wojtekerbetowski](https://github.com/wojtekerbetowski) for marking this problem and organizing [Name Collision](https://www.hackerleague.org/hackathons/name-collision) on which we have started work on this script. 
