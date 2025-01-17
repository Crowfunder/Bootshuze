import re
import gc
import os.path
import PySimpleGUI as sg
from os import mkdir as mkdir
from wget import download as download_file

# Used for downloading missing template files.
def templates_download():

  dl_urls = [
    "https://raw.githubusercontent.com/Crowfunder/Bootshuze-GUI/master/templates/template_articulated",
    "https://raw.githubusercontent.com/Crowfunder/Bootshuze-GUI/master/templates/template_static"
  ]

  if not os.path.isdir("templates") == True:
    mkdir("templates")
  
  sg.Popup('Downloading template files...', button_type=5, 
            auto_close=True, no_titlebar=True)

  for url in dl_urls:
    download_file(url, out = "templates/")


# Allows printing directly into window console.
def console_print(text, window):
  print(text)
  window.Refresh()


def main(file, file_name, window, template):
  
  with open(file, 'r') as f:
    args     = dict()
    faces    = list()
    indices  = list()
    vertices = list()
    lines = f.readlines()
    
    console_print('Reading input model file.', window)
    console_print('Calculating indices...', window)
    
    for line in lines:
      # Store faces that determine the numbers for indices
      if line[0] == 'f':
        if 'mode' not in args:
          indices_count = len(line.split()[1:])
          if indices_count == 2: args['mode'] = 'LINES'
          if indices_count == 3: args['mode'] = 'TRIANGLES'
          if indices_count == 4: args['mode'] = 'QUADS'
          
        for face in line.split()[1:]:
          if face not in faces: faces.append(face.replace('\n', ''))
          indices.append(faces.index(face))
      
      # Calculate min/max extent for vertices
      if line[:2] == 'v ':
        # Initialize values with first vertex
        if 'min_extent' not in vars() and 'max_extent' not in vars():
          min_extent = [float(val) for val in line.split()[1:]]
          max_extent = [float(val) for val in line.split()[1:]]
        
        # And change values as we go through other vertices  
        for index, vertex in enumerate(line.split()[1:]):
          min_extent[index] = min(min_extent[index], float(vertex))
          max_extent[index] = max(max_extent[index], float(vertex))
    
    vt = list(filter(lambda x: x[:2] == 'vt', lines))
    vn = list(filter(lambda x: x[:2] == 'vn', lines))
    v  = list(filter(lambda x: x[:2] == 'v ', lines))
    
    if len(vt) == 0:
      raise Exception('Input model lacks UV mapping. '
                      'Model cannot be correctly created.')
    
    console_print('Calculating vertices...', window)
    
    # Generate vertices list based on indices from input file
    for face in faces:
      face_indices = face.split('/')
      
      # Texture coordinates, UV
      vertices.extend(vt[int(face_indices[1])-1].split()[1:])
      
      # Face normals
      vertices.extend(vn[int(face_indices[2])-1].split()[1:])
      
      # Position coordinates, XYZ
      vertices.extend(v [int(face_indices[0])-1].split()[1:])
    
    del faces
    del lines
    del v, vn, vt
    
  with open(f"{file_name}.xml", 'w+') as o, \
       open(f"templates/{template}", 'r') as i:
    console_print(f'Writing output with {template}...', window)
    
    args['min_extent'] = str(min_extent)[1:-1]
    del min_extent
    args['max_extent'] = str(max_extent)[1:-1]
    del max_extent
    args['indices']    = str(indices)[1:-1]
    args['indices_end'] = str(max(indices))
    del indices
    args['vertices']   = ', '.join(vertices)
    del vertices
    gc.collect()
    
    regex = re.compile(r'(?:{{ )([a-zA-Z_]*)(?: }})')
    for line in i:
      if any(f'{{ {arg} }}' in line for arg in args.keys()):
        line = regex.sub(args[regex.search(line).group(1)], line)
      o.write(line)
      
    console_print(f'Finished writing to {o.name}.', window)
    console_print(f'Done!', window)
    window['_done_'].Update('Done!')

  
def menu():

  column1 = [
              [sg.Text('Welcome to Bootshuze-GUI!', size=(24,1), 
                        justification='c', font=('Helvetica', 15))],
              [sg.Text('Select a .obj model to process:')], 
              [sg.InputText(size=(29,1)), 
                sg.FileBrowse(file_types=(("Wavefront Files", "*.obj"),))],
              [sg.Radio('Articulated','OUTPUT_TYPE', default=True,
                        tooltip='Output model as Articulated type',
                        key='_articulated-mode_'),
                sg.Radio('Static', 'OUTPUT_TYPE', key='_static-mode_', 
                        tooltip='Output model as Static type')],
              [sg.Button('Submit'), 
                sg.Text('', text_color='lawn green', key='_done_',
                        size=(5,1))]
            ]

  column2 = [
              [sg.Output(size=(36,6), key='_output_')],
              [sg.Button('Clear Console')]
            ]

  layout = [[sg.Frame(layout = column1, title='')], 
            [sg.Frame(layout = column2, title='Console')]]

  window = sg.Window('Bootshuze-GUI v1.1.0', layout, 
                      element_justification='c').Finalize()
      

  while True:
    try:
          
      event, values = window.Read()
      if event is None:
        break

      elif event == 'Submit':
        file = values[0]
        window['_done_'].Update('')
              
        if window['_articulated-mode_'].Get() == True:
          template = "template_articulated"
        elif window['_static-mode_'].Get() == True:
          template = "template_static"

        file_name = os.path.basename(file).replace('.obj', '')
        if os.path.isfile(f'{file_name}.xml'):
          console_print(f'File {file_name}.xml '
                         'already exists! Halting!', window)

        else:
          if file != '':
            console_print(fr'''Processing "{file}"...''', window)
            main(file, file_name, window, template)
          else:
            raise Exception('Please select a file!')
          console_print('---------------------------------'
                        '------------------------------', window)

      elif event == 'Clear Console':
              window['_output_'].Update('')
              
    except Exception as e:
      console_print(e, window)
      console_print('---------------------------------'
                    '------------------------------', window)


if __name__ == '__main__':

  if not os.path.isfile('templates/template_articulated'):
    if not os.path.isfile('templates/template_static'):
      try:
        templates_download()
      except:
        sg.PopupError("Template files are missing, make " 
                      "sure they are in the same directory "
                      "as this script and start again.")  
        quit()

  menu()
