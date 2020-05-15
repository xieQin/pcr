package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
)

var version string = "v1"

// User struct
type User struct {
	QQID     int    `json:"qqid"`
	NickName string `json:"nickname"`
	SL       *int   `json:"sl"`
}

// UserChallenge struct
// "boss_num": 5,
// "challenge_time": 1589294527,
// "comment": {
// 	"behalf": "\u7531\u6e05\u971c\u4ee3\u62a5\u3002"
// },
// "cycle": 3,
// "damage": 121449,
// "health_ramain": 12640002,
// "is_continue": false,
// "message": "",
// "qqid": 3150539648
type UserChallenge struct {
	BossNum       int `json:"boss_num"`
	ChallengeTime int `json:"challenge_time"`
	Comment       struct {
		BeHalf string `json:"behalf"`
	} `json:"comment"`
	Cycle       int    `json:"cycle"`
	Damage      int    `json:"damage"`
	HealthRamin int    `json:"health_ramain"`
	IsContinue  bool   `json:"is_continue"`
	Message     string `json:"message"`
	QQID        int    `json:"qqid"`
}

// UserChallengeTotal struct
type UserChallengeTotal struct {
	QQID     int    `json:"qqid"`
	Damage   int    `json:"damage"`
	NickName string `json:"nickname"`
}

// UserChallengeTotalSlice type
type UserChallengeTotalSlice []UserChallengeTotal

func (s UserChallengeTotalSlice) Len() int           { return len(s) }
func (s UserChallengeTotalSlice) Swap(i, j int)      { s[i], s[j] = s[j], s[i] }
func (s UserChallengeTotalSlice) Less(i, j int) bool { return s[i].Damage > s[j].Damage }

// Marshal func
func Marshal(data interface{}) []byte {
	res, err := json.Marshal(data)
	if err != nil {
		log.Fatal(err)
	}
	return res
}

// Unmarshal func
func Unmarshal(data []byte, res interface{}) {
	err := json.Unmarshal(data, &res)
	if err != nil {
		log.Fatal(err)
	}
}

// ReadFile func
func ReadFile(path string, bytes int32) []byte {
	fp, err := os.OpenFile(path, os.O_RDONLY, 0755)
	defer fp.Close()
	if err != nil {
		log.Fatal(err)
	}
	data := make([]byte, bytes)
	n, err := fp.Read(data)
	if err != nil {
		log.Fatal(err)
	}
	return data[:n]
}

// WriteFile func
func WriteFile(path string, data []byte) {
	fp, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE, 0755)
	if err != nil {
		log.Fatal(err)
	}
	defer fp.Close()
	_, err = fp.Write(data)
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	userData := ReadFile("./data/"+version+"/user.json", 10000)
	userChallengeData := ReadFile("./data/"+version+"/challenge.json", 1000000)
	var users []User
	var challenges []UserChallenge
	Unmarshal(userData, &users)
	Unmarshal(userChallengeData, &challenges)
	fmt.Println(users)
	fmt.Println(challenges)

	results := map[string]*UserChallengeTotal{}

	for _, user := range users {
		qqid := strconv.Itoa(user.QQID)
		results[qqid] = &UserChallengeTotal{
			QQID:     user.QQID,
			Damage:   0,
			NickName: user.NickName,
		}
	}

	for _, challenge := range challenges {
		qqid := strconv.Itoa(challenge.QQID)
		_, ok := results[qqid]
		if ok {
			damage := challenge.Damage
			results[qqid].Damage += damage
		}
	}

	fmt.Println(results)
	// var sortedRes UserChallengeTotalSlice
	sortedRes := make(UserChallengeTotalSlice, 0)
	for _, res := range results {
		item := UserChallengeTotal{
			Damage:   res.Damage,
			QQID:     res.QQID,
			NickName: res.NickName,
		}
		sortedRes = append(sortedRes, item)
	}
	sort.Stable(sortedRes)

	// fmt.Println(sortedRes)

	for _, i := range sortedRes {
		fmt.Println("昵称：", i.NickName, "，伤害：", i.Damage)
	}

	data := Marshal(sortedRes)
	WriteFile("./res/results"+version+".json", data)
}
