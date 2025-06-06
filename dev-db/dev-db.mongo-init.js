db.createUser({
  user: "admin",
  pwd: "admin",
  roles: [
    {
      role: "readWrite",
      db: "strava",
    },
  ],
});

db = db.getSiblingDB("strava");

db.createCollection("users");
db.createCollection("sync_metadata");
db.createCollection("activities");
