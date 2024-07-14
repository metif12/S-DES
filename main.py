
p_10 = [3,5,2,7,4,10,1,9,8,6]
p_08 = [6,3,7,4,8,5,10,9]
p_04 = [2,4,3,1]
expand = [4,1,2,3,2,3,4,1]
ip = [2,6,3,1,4,8,5,7]
ip_inverse = [4,1,3,5,7,2,8,6]

s_box1 = [ [1,0,3,2],
						[3,2,1,0],
						[0,2,1,3],
						[3,1,3,2] ]

s_box2 = [ [0,1,2,3],
						[2,0,1,3],
						[3,0,1,0],
						[2,1,0,3] ]


def permute(vector, permutation):
  return [vector[i-1] for i in permutation]


def shift(vector):
  shifted = [v for v in vector[1:]]
  shifted.append(vector[0])
  return shifted

def input_vector(length, name):
  while True:
    text = input(f"Please enter your {name}: ")
    
    if not len(text) == length:    
      print(f"Wrong {name}!")
      continue
    
    if not text.isdigit():    
      print(f"Wrong {name}!")
      continue

    vector = [int(k) for k in text]
     
    for k in vector:
      if k > 1:    
        print("Wrong key!")
        continue
      
    return vector

def swap(vector):
  parts = split(vector)

  return parts[1] + parts[0]

def split(vector):
  i = len(vector) // 2

  return (vector[0:i], vector[i:])

def keys(key_vector):
  p10key = permute(key_vector, p_10)
  
  left,right = split(p10key)
  left_shifted = shift(left)
  right_shifted= shift(right)
  combined = left_shifted+right_shifted
    
  p8key1= permute(combined,p_08)
  
  left,right = split(combined)
  left_shifted = shift(left)
  right_shifted= shift(right)
  combined = left_shifted+right_shifted
  
  p8key2= permute(combined,p_08)
  
  return (p8key1,p8key2)

def xor(vector1,vector2):
  return [ 1 if vector1[i] ^ vector2[i] else 0 for i in range(len(vector1)) ]

def sbox(box, vector):
  i = vector[3] * 2 + vector[0]
  j = vector[2] * 2 + vector[1]
  
  v = box[i][j]
  
  return [v//2, v%2]  
  
def f(right,key):
  right_expanded = permute(right, expand)
  key1xor = xor(right_expanded,key)
  s1,s2 = split(key1xor)
  s0sbox = sbox(s_box1,s1)
  s1sbox = sbox(s_box2,s2)
  
  combine = s0sbox + s1sbox
  
  p4vec = permute(combine, p_04)
  
  return p4vec
  
def fkey(left,right,key):
  f_r_key = f(right,key)
  return xor(left,f_r_key)

def encrypt(vector, key1, key2):
  ip_vector = permute(vector, ip)
  
  left,right = split(ip_vector)
  fkey1 = fkey(left,right,key1)
  combined = fkey1+right
  
  swaped = swap(combined)
  
  left,right = split(swaped)
  fkey2 = fkey(left,right,key2)
  combined = fkey2+right
  
  ip_inverse_vector = permute(combined,ip_inverse)
  
  return ip_inverse_vector

def decrypt(vector, key1, key2):
  ip_vector = permute(vector, ip)
  
  left,right = split(ip_vector)
  fkey2 = fkey(left,right,key2)
  combined = fkey2+right
  
  swaped = swap(combined)
  
  left,right = split(swaped)
  fkey1 = fkey(left,right,key1)
  combined = fkey1+right

  ip_inverse_vector = permute(combined,ip_inverse)
  
  return ip_inverse_vector
  
def main():
  key_vector = input_vector(10, "KEY")
  key1,key2 = keys(key_vector)

  print("KEY1: ", key1)
  print("KEY2: ", key2)
  print()

  while True:
    print("MENU:\n1.Encrypt\t2.Decrypt\t3.Exit")

    choice = input("Enter your choice: ")

    if choice == "3":
      print("Goodbye.")
      break

    elif choice == "1":
      plain_vector = input_vector(8,"Plain")
      decrypted = encrypt(plain_vector,key1,key2)
      print("Encrypted: ", decrypted)

    elif choice == "2":
      encrypted_vector = input_vector(8,"Encrypted")
      decrypted = decrypt(encrypted_vector,key1,key2)
      print("Decrypted: ", decrypted)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("Goodbye.")
  except Exception as e:
    print("something went wrong!")
