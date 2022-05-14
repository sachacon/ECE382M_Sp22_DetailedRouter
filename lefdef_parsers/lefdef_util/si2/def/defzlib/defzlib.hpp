// *****************************************************************************
// *****************************************************************************
// Copyright 2012, Cadence Design Systems
// 
// This  file  is  part  of  the  Cadence  LEF/DEF  Open   Source
// Distribution,  Product Version 5.8. 
// 
// Licensed under the Apache License, Version 2.0 (the "License");
//    you may not use this file except in compliance with the License.
//    You may obtain a copy of the License at
// 
//        http://www.apache.org/licenses/LICENSE-2.0
// 
//    Unless required by applicable law or agreed to in writing, software
//    distributed under the License is distributed on an "AS IS" BASIS,
//    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
//    implied. See the License for the specific language governing
//    permissions and limitations under the License.
// 
// For updates, support, or to become part of the LEF/DEF Community,
// check www.openeda.org for details.
// 
//  $Author: dell $
//  $Revision: #7 $
//  $Date: 2015/01/27 $
//  $State:  $
// *****************************************************************************
// *****************************************************************************

#ifndef LEFDEFZIP_H
#define LEFDEFZIP_H

typedef void* defGZFile;

/* 
 * Name: defGZipOpen
 * Description: Open a gzip file
 * Returns: A file pointer
 */
extern defGZFile defGZipOpen(const char* gzipFile, const char* mode);

/* 
 * Name: defGZipClose
 * Description: Close a gzip file
 * Returns: 0 if no errors
 */
extern int defGZipClose(defGZFile filePtr);

/*
 * Name: defrReadGZip
 * Description: Parse a def gzip file
 * Returns: 0 if no errors
 */
extern int defrReadGZip(defGZFile file, const char* gzipFile, void* uData);

#endif
