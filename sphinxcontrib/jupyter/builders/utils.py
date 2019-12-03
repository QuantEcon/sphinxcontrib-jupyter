""""
Utility functions used primarily in builders
""""

def create_codetree_ds(self, codetree_ds, cell):
    codetree_ds[cell.metadata.hashcode] = dict()
    key = codetree_ds[cell.metadata.hashcode]
    if hasattr(cell, 'source'): key['source']= cell.source
    if hasattr(cell, 'outputs'): key['outputs'] = cell.outputs
    return codetree_ds
    

def normalize_cell(self, cell):
    cell.source = cell.source.strip().replace('\n','')
    return cell
    
def create_hash(self, cell):
    hashcode = md5(cell.source.encode()).hexdigest()
    cell.metadata.hashcode = hashcode
    return cell

def create_hashcode(self, cell):
    hashcode = md5(cell.source.encode()).hexdigest()
    return hashcode

def copy_dependencies(builderSelf, outdir = None):
    """
    Copies the dependencies of source files or folders specified in the config to their respective output directories
    """
    if outdir is None:
        outdir = builderSelf.outdir
    else:
        outdir = outdir
    srcdir = builderSelf.srcdir
    if 'jupyter_dependencies' in builderSelf.config and builderSelf.config['jupyter_dependencies'] is not None:
        depenencyObj = builderSelf.config['jupyter_dependencies']
        for key, deps in depenencyObj.items():
            full_src_path = srcdir + "/" + key
            if full_src_path.find('.') == -1:
                ## handling the case of key being a directory
                full_dest_path = outdir + "/" + key
                ensuredir(full_dest_path)
                for dep in deps:
                    copy(full_src_path + "/" + dep, full_dest_path,follow_symlinks=True)
            elif os.path.isfile(full_src_path):
                ## handling the case of key being a file
                # removing the filename to get the directory path
                index = key.rfind('/')
                if index!=0 and index != -1:
                    key = key[0:index]
                
                full_src_path = srcdir + "/" + key
                full_dest_path = outdir + "/" + key
                for dep in deps:
                    copy(full_src_path + "/" + dep, full_dest_path,follow_symlinks=True)