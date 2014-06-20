from PIL import Image;
import os;
import math;
import json;
loaded = [];
used = [];
size = 0;
index = int;
def order(directory, *images):
    os.chdir(directory)
    while True:
        size = 0;
        for i in range(len(images)):
            if i not in used:
                img = Image.open(images[i]);
                volume = img.size[0] * img.size[1];
                if volume >= size:
                    size = volume;
                    index = i;
        used.append(index);
        loaded.append({'name': images[index], 'w': int(img.size[0]), 'h': int(img.size[1])});
        if len(loaded) == len(images):
            return(loaded);
            break;
class BinaryTree:
    def __init__(self,rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self,newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self,newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self,obj):
        self.key = obj

    def getRootVal(self):
        return self.key


class packer(BinaryTree):
    def __init__(self, w, h):
        self.w = w;
        self.h = h;
        self.count = 0;
        self.pos = [];
    def fit(self, blocks):
        self.pos = [];
        r = BinaryTree({'x': 0, 'y': 0, 'w': self.w, 'h': self.h, 'used': False});
        for block in blocks:
            self.count = 0;
            block['fit'] = self.findNode(r, block['w'], block['h'], block['name']);
        return(self.pos);
    def findNode(self, r, w, h, name):
        root = r.getRootVal();
        if root['used'] == True:
            self.findNode(r.getLeftChild(), w, h, name);
            self.findNode(r.getRightChild(), w, h, name);
        elif w <= root['w'] and h <= root['h']:
            if self.count == 0:
                self.count = 1;
                root['used'] = True;
                r.insertLeft({'x': root['x'], 'y': root['y'] + h, 'w': root['w'], 'h':  root['h'] - h, 'used': False});
                r.insertRight({'x': root['x'] + w, 'y': root['y'], 'w': root['w'] - w, 'h': h, 'used': False});
                fit = {'x': root['x'], 'y': root['y'], 'w': w, 'h': h, 'name': name};
                self.pos.append(fit);

def create(directory, name):
    total_vol = 0;
    maxed = False;
    w_maxed = False;
    h_maxed = False;
    items = order(directory, 'new.png', 'test2.JPG', 'tester.png', 'testing.png', 'shoe.JPG');
    for i in range(len(items)):
        total_vol += items[i]['w'] * items[i]['h'];
    img_w = math.floor(math.sqrt(total_vol));
    img_h = math.floor(math.sqrt(total_vol));
    while True:
        test = packer(img_w, img_h);
        if len(test.fit(items)) < len(items) and maxed == False:
            img_w += 1;
            img_h += 1;
        else:
            maxed = True;
            if len(test.fit(items)) == len(items) and w_maxed == False and maxed == True:    
                img_w -= 1;
            else:
                w_maxed = True;
                if len(test.fit(items)) == len(items) and h_maxed == False and maxed == True:
                    img_h -= 1;
                else:
                    h_maxed = True;
                    if w_maxed == True and h_maxed == True:
                        img_w += 1;
                        test = packer(img_w, img_h);
                        img = Image.new('RGBA', (int(img_w), int(img_h)), 'white');
                        Json = {};
                        for i in test.fit(items):
                            imgs = Image.open(i['name']);
                            img.paste(imgs, (i['x'], i['y']));
                            Json[i['name']] = {'x': i['x'], 'y': i['y'], 'h': i['h'], 'w': i['w']};
                        os.chdir(directory);
                        img.save(name + '.png');
                        jsonFile = open(name + '.json', 'w+');
                        json.dump(Json, jsonFile);
                        print(img_w, img_h);
                        print(test.fit(items));
                        break;
create('/Users/Sea_Snell/Documents/python/texture_packer', 'test');
