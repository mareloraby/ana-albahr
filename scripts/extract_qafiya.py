import pandas as pd
import pyarabic.araby as araby


def clean_poems(poem):
    clean_poem = ''
    poem_lines = poem.split('\n')
    num_lines = len(poem_lines)
    
    for line_id in range(0,num_lines):
        line = araby.strip_tashkeel(poem_lines[line_id])
        line = araby.strip_tatweel(line)
        clean_poem += line
        
        if(not(num_lines == line_id+1)):
            clean_poem += '\n'
            
    return clean_poem


def list_to_str(lines_list):
    poem = ''
    
    for line_id in range(0, len(lines_list)):
        poem += lines_list[line_id]
        if(not(len(lines_list) == line_id+1)):
            poem += '\n'
    return poem


def create_new_df(extracted_qafiyas):
    
    qafya1 = []
    qafya2 = []
    poems = []
    for qafya_list in extracted_qafiyas:
        
        qafya1.append(qafya_list[0])
        qafya2.append(qafya_list[1])
       
        poems.append(qafya_list[2])
     
    df = pd.DataFrame({'poem': poems,
                       'qafya1':qafya1,
                       'qafya2':qafya2})
    
    return df
        

def extract_qafyas(poems):
    
    available_qafiyas = []
    bad_poems=[]
    for poem_id in range(0, len(poems)):

        try:
            idx = 1
            lines= poems[poem_id].split('\n')
            while(idx < len(lines)-2):
                qafiyas = []
                qafiya1 = lines[idx].split()[-1][-1]

                qafiyas.append(qafiya1)
                idx+=2
                qafiya2 = lines[idx].split()[-1][-1]
                qafiyas.append(qafiya2)
                poem_lines = lines[idx-3:idx+1]
                poem = list_to_str(poem_lines)
                qafiyas.append(poem)
                available_qafiyas.append(qafiyas)
                idx+=2
        
        except:
            
            bad_poems.append(poem_id)
            
            
    return bad_poems, available_qafiyas



data = pd.read_csv('Arabic_poetry_dataset_clean.csv')
data['clean_poem'] = data['poem_text'].apply(clean_poems) 

# data.to_csv('Arabic_poetry_dataset_clean.csv')

poems = list(data.clean_poem.values)
bad_poems, available_qafiyas = extract_qafyas(poems)




new_df = create_new_df(available_qafiyas) 
new_df.to_csv('qafya_poetry.csv')

with open('bad_poems.txt', 'w') as file:
    for index in bad_poems:
        file.write(str(index))
    file.close()


        
        
        
        
        
        

