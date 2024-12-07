# GTA V FiveM Meta File Conflict Resolution Tool Requirements

## Overview
A tool to resolve conflicts in GTA V FiveM meta files by managing carcols IDs and modkit IDs across multiple files.

## Core Features

### 1. Carcols Confliction Resolution
#### Functional Requirements
- Must process both carcols.meta and carvariations.meta files
- Must support both single vehicle and batch (all vehicles) processing
- Must generate unique random numbers for carcols IDs
- Must maintain ID consistency across both files
- Must preserve all other XML structure and content

#### Technical Requirements
- Input: carcols.meta and carvariations.meta files
- Process:
  1. Locate `<id value="X"/>` in carcols.meta
  2. Generate new random number
  3. Replace old ID with new number
  4. Locate corresponding `<sirenSettings value="X"/>` in carvariations.meta
  5. Replace with same new number
- Output: Modified meta files with updated IDs

### 2. Modkit ID Confliction Resolution
#### Functional Requirements
- Must process both carcols.meta and carvariations.meta files
- Must support both single vehicle and batch processing
- Must generate valid modkit IDs (2-6 digits)
- Must maintain consistency across both files
- Must update both the kitName and associated ID values

#### Technical Requirements
- Input: carcols.meta and carvariations.meta files
- Process:
  1. Locate modkit patterns in carcols.meta:
     ```xml
     <kitName>XXX_name_modkit</kitName>
     <id value="XXX" />
     ```
  2. Generate new ID number (2-6 digits)
  3. Update both values in carcols.meta
  4. Locate corresponding pattern in carvariations.meta:
     ```xml
     <kits>
       <Item>XXX_name_modkit</Item>
     </kits>
     ```
  5. Update with same new ID

## User Interface Requirements
- Must be easy to understand for end-users
- Must allow selection of input files
- Must provide option to process single vehicle or all vehicles
- Must show clear feedback on changes made
- Must provide backup of original files

## Technical Implementation Requirements
- Must be open source
- Must handle XML parsing safely
- Must validate input files
- Must maintain XML formatting
- Must handle errors gracefully
- Must provide clear error messages
