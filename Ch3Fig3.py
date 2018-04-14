#invert the c matrix produced by Ch3Fig2
ci=np.linalg.inv(c)/10000
print("    ",ci[0])
print(f'C\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}=',ci[1],"    (3.17)")
print("    ",ci[2])
