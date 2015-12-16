// Copyright 2015 Michael Gugino
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <Python.h>
#include <string.h>
#include <stddef.h>

static PyObject*
parse_qs(PyObject* self, PyObject* args)
{
  char *qs;
  char *localqs;
  char *freeqs;
  char *token;
  char *tokena;



  if (!PyArg_ParseTuple(args, "s", &qs))
      return NULL;
  freeqs = localqs = strdup(qs);
  if (localqs == NULL) {
    PyErr_SetString(PyExc_RuntimeError, "Unable to malloc");
    return NULL;
  }
  PyDictObject *d = PyDict_New();

    while ((token = strsep(&localqs, "&")) != NULL) {
          tokena = strsep(&token, "=");

          if (token == NULL)
            PyDict_SetItem(d, PyString_FromString(tokena), PyString_FromString(""));
          else {
            PyDict_SetItem(d, PyString_FromString(tokena), PyString_FromString(token));
          }

    }

    free(freeqs);
    return d;
}

static PyMethodDef QSMethods[] =
{
     {"parse_qs", parse_qs, METH_VARARGS, "Parse a string"},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initqs_parse(void)
{
     (void) Py_InitModule("qs_parse", QSMethods);
}
