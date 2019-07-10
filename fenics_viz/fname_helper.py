import os

def get_fnames(extensions_required, files, directory):

    fnames = len(extensions_required) * [None]

    if len(files) != len(extensions_required):
        raise SystemError("Must select " + str(len(extensions_required)) + " files: " + str(extensions_required))

    for filename in files:
        full_name = os.path.join(directory, filename.name)
        extension = get_extension(full_name)
        if not extension in extensions_required:
            raise SystemError("Allowed extensions are: " + str(extensions_required) + " but chosen is: " + str(extension))

        idx = extensions_required.index(extension)
        fnames[idx] = full_name

    # Check all extensions are present
    for fname in fnames:
        if fname == None:
            raise SystemError("Missing files! Required are: " + str(extensions_required) + " but got: " + str(fnames))

    return fnames

def get_extension(fname):
    _, extension = os.path.splitext(fname)
    return extension

def get_base_name(fname):
    # Remove leading directories
    base = os.path.basename(fname)
    # Remove extension
    filename, _ = os.path.splitext(base)
    return filename
