# Docker Configuration

This folder contains Docker-related configuration files for the Finance Tracker project.

## Structure

```
docker/
├── postgres/
│   ├── init.sql          # PostgreSQL initialization script
│   └── data/             # PostgreSQL data (auto-created, in .gitignore)
└── README.md             # This file
```

## PostgreSQL Initialization

The `init.sql` script runs automatically when the PostgreSQL container is created for the first time. It:

- Creates useful PostgreSQL extensions
- Sets the timezone to Asia/Kolkata
- Logs initialization status

## Data Persistence

PostgreSQL data is stored in a Docker volume named `postgres_data`. This ensures your data persists even when containers are stopped or removed.

**To view volumes:**
```bash
docker volume ls
```

**To inspect the volume:**
```bash
docker volume inspect finance-tracker_postgres_data
```

**To backup the volume:**
```bash
docker run --rm -v finance-tracker_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

**To restore the volume:**
```bash
docker run --rm -v finance-tracker_postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /data
```

## Useful Commands

See `DOCKER_QUICK_START.md` in the project root for common commands.
