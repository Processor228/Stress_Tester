import subprocess


class DbRoom:

    def __init__(self, b, tg, te):

        self.bruteforce_src: str = b
        self.test_gen_src: str = tg
        self.tested_src: str = te


CONTAINERS_NOW = 1

db_room = DbRoom("""
#include<bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    sort(a.begin(), a.end());
       //  [](int a, int b){
        //return a > b;
    //});

    for (auto i : a) {
        cout << i << " ";
    }
    cout << '\\n';
}
"""
,
                 """#include <bits/stdc++.h>
using namespace std;

uint64_t timeSinceEpochMillisec() {
    using namespace std::chrono;
    return duration_cast<milliseconds>(system_clock::now().time_since_epoch()).count();
}

auto main () -> int {
    srand(timeSinceEpochMillisec());
    int numbers = 1 + rand() % 20;
    cout << numbers << "\\n";
    while (numbers--) {
    cout << -20 + rand() % 101 << " ";
    }
    cout << "\\n";

    return EXIT_SUCCESS;
};""",

"""#include <bits/stdc++.h>
using namespace std;

auto main () -> int {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    for (int i = 0; i < a.size(); i++) {
        for (int j = i; j < a.size(); j++) {
            if (a[i] < a[j])
                swap(a[i], a[j]);
            }
    }

    for (auto i : a) {
        cout << i << " ";
    }
    cout << "\\n";
};
""")

# import json
# print(json.)

# subprocess.run(["mkdir", "test_dir/stress{}".format(CONTAINERS_NOW)])
#
# with open("test_dir/stress{}/bruteforce_src.cpp".format(CONTAINERS_NOW), "w") as wr:
#     wr.write(db_room.bruteforce_src)
# with open("test_dir/stress{}/test_gen_src.cpp".format(CONTAINERS_NOW), "w") as wr:
#     wr.write(db_room.test_gen_src)
# with open("test_dir/stress{}/tested_src.cpp".format(CONTAINERS_NOW), "w") as wr:
#     wr.write(db_room.tested_src)
#
# subprocess.run("cat test_script.sh > test_dir/stress{}/test.sh".format(CONTAINERS_NOW), shell=True)
# subprocess.run("cat test_Dockerfile > test_dir/stress{}/Dockerfile".format(CONTAINERS_NOW), shell=True)
#
# # --------------( building the image )------------------ #
# subprocess.run(
#     ["docker", "build", "-t", "stress_{}".format(CONTAINERS_NOW), "test_dir/stress{}".format(CONTAINERS_NOW)])
#
# # ------------ ( starting the container) --------------- #
# container_id = str(subprocess.check_output(
#     ["docker", "run", "-t", "-d", "stress_{}:latest".format(CONTAINERS_NOW)]))[2:-3]
# print(container_id)
#
# # ------------ ( invoking testing procedure ) ---------- #
# result = subprocess.check_output(["docker", "exec", container_id, "bash", "test.sh"])
# print(result.decode("utf-8"))
#
# subprocess.run(["docker", "kill", container_id])
print(str(db_room.tested_src.encode())[2:-3])
print(str(db_room.test_gen_src.encode())[2:-3])
print(str(db_room.bruteforce_src.encode())[2:-3])

