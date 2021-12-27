# read file
with open(r"FONTS.txt", 'r') as fp:
    # read an store all lines into list
    lines = fp.readlines()
counter = 0
# Write file
range(6,6671,8)
tff=[]
with open(r"newFonts.txt", 'w') as fp:
    # iterate each line
    for number, line in enumerate(lines):
        # delete line 5 and 8. or pass any Nth line you want to remove
        # note list index starts from 0
        if number in range(1,2501,3):
            tff.append(line)

    for number, line in enumerate(lines):
        
        # delete line 5 and 8. or pass any Nth line you want to remove
        # note list index starts from 0
        if number in range(0,2501,3):
            new_line= '"'+line.rstrip("\n")+'"'+": "+'"'+tff[counter].rstrip("\n")+'"'+","+"\n"
            counter+=1
            print (new_line)
            fp.write(new_line)

