# Habit Tracker

## About The Project

```mermaid
---
title: notion-habit classes
---
classDiagram

    class NotionHabit{
        String id_
        String date_
        String tags_
        String status_
        parse_json()
        update_status()
        get_name() 
        get_id()
        get_date()
        get_tags()
        get_status()
    }

    class NotionHabitUtils{
        logging.Logger logger
        response_error()
        query_habit()
        unique_habit()
        update_habit()
        log_json()
    }
    
    class NotionHabitAnalyzer{
        logging.Logger logger
        NotionHabitUtils utils
        analyze_habit()
        generate_analyze_table()
    }

    class NotionHabitCLI{
        argparse.ArgumentParser parser
        logging.Logger logger
        NotionHabitAnalyzer analyzer
        NotionHabitUtils utils
        create_parser()
        run()
    }

    class NotionHabitQT{

    }

```


## Getting Started

### Prerequistes

### Installation

## Usage 

## Roadmap

